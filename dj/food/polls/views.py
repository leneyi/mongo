import json
import textwrap
import time
from threading import Thread

import datetime

from django.core.serializers.json import DjangoJSONEncoder

from src.main.run import wechat
from src.main.server import WechatData
from pprint import pprint
from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from django.views.decorators.http import require_http_methods
from . import models
from django.utils import timezone


def index(request):
  return HttpResponse("Hello, world. You're at the polls index.")
  # return render(request, 'hello.html')


def ceil_dt(dt):
  # how many secs have passed this hour
  nsecs = dt.minute * 60 + dt.second + dt.microsecond * 1e-6
  # number of seconds to next quarter hour mark
  # Non-analytic (brute force is fun) way:
  #   delta = next(x for x in xrange(0,3601,900) if x>=nsecs) - nsecs
  # analytic (ARGV BATMAN!, what is going on with that expression) way:
  delta = (nsecs // 900) * 900 + 900 - nsecs
  # time + number of seconds to quarter hour mark.
  return dt + datetime.timedelta(seconds=delta)


class HourMinuteSerializer(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      return obj.strftime('%H:%M')
    elif isinstance(obj, datetime.date):
      return obj.strftime('%Y-%m-%d')
    # Let the base class default method raise the TypeError
    return json.JSONEncoder.default(self, obj)


def reserve(request):
  print(request.POST)
  try:
    (hour, minute) = request.POST['time'].split(":")
    guest_num = request.POST['guest_num']
    openid = request.POST['openid']
    print(hour, minute)
  except KeyError:
    return HttpResponse("Invalid form!")
  else:
    reserve_time = timezone.now()
    new_time = reserve_time.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
    # print(new_time)
    try:
      user = models.WechatUser.objects.get(pk=openid)
      reservations = models.Reservation.objects.filter(reserver=user)
      if len(reservations) > 0:
        reservation = reservations[0]
        return HttpResponse("You already had a reservation at {} with {} guests.".format(reservation.get_time(),
                                                                                         reservation.get_guest_num()))

      new_reservation = models.Reservation(reserver=user, arrival_time=new_time, guest_num=guest_num)

      new_reservation.save()
      return HttpResponse("Thank you!")
    except models.WechatUser.DoesNotExist:
      return HttpResponse("User not found!")


def api(request, model):
  from_time = request.GET.get('time')
  if model == models.Reservation.__name__ and from_time == 'fromNow':
    # TODO: Make sure options are are within the same day, or some way to distinguish them.
    now = datetime.datetime.now()
    incoming_quarter = ceil_dt(now)
    options = [incoming_quarter + datetime.timedelta(seconds=900 * i) for i in range(8)]
    # output = ["{}:{}".format(t.hour, t.min) for t in options]
    print(now, options)
    return HttpResponse(json.dumps(options, cls=HourMinuteSerializer))
  # print question_id
  print "Model:", model
  reservations = models.__dict__[model].objects.all()
  print reservations
  data = serializers.serialize("json", reservations)
  return HttpResponse(data)


@require_http_methods(["GET", "POST"])
def verify(request):
  timestamp = request.GET.get('timestamp')
  signature = request.GET.get('signature')
  nonce = request.GET.get('nonce')
  pprint(request.GET)
  # pprint(request.body)
  if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
    print "valid request"
    echostr = request.GET.get('echostr')
    print request.body

    if echostr:
      return HttpResponse(echostr)
    else:
      # request.body contains the message xml
      msg = WechatData(request.body)
      # process_msg(msg)
      if msg.is_text_msg() or msg.is_subscribe_event():
        async_send_message(msg.get_from_user_name(),
                           "http://wechat.grabbieteam.com/static/html/reserve.html?openid={}".format(
                             msg.get_from_user_name()))
      return HttpResponse(" ")
  else:
    print "invalid request"
    return HttpResponse(status=406)


def get_help_command():
  return textwrap.dedent("""\
  1: Make a reservation.
  2: Cancel an existing reservation.""")


def process_msg(msg):
  ERROR_MSG = "Unrecognized command. Please make sure to type a number."

  def try_to_reserve(msg, user):
    try:
      num_guest = int(msg.get_content())
    except ValueError:
      async_send_message(user.get_id(), "{}\n{}".format(ERROR_MSG, get_help_command()))
    else:
      async_send_message(user.get_id(), "What time?")

  print("from open id: {}".format(msg.get_from_user_name()))
  user = models.WechatUser.objects.get(pk=msg.get_from_user_name())

  state_to_func = {models.Status.INIT: try_to_reserve}

  state_to_func[user.get_state()](msg, user)


def print_func(times):
  for i in range(times):
    print "hi there!"
    time.sleep(1)


def async_send_message(open_id, text):
  t = Thread(target=send_message, args=(open_id, text))
  t.start()


def send_message(username, text):
  wechat.send_text_message(username, text)
