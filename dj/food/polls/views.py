import datetime
import json
import textwrap
import time
from pprint import pprint

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_http_methods

from polls import models
from polls.util import async_send_message
from src.main.run import wechat
from src.main.server import WechatData


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
    time_str = request.POST['time']
    guest_num = request.POST['guest_num']
    openid = request.POST['openid']
  except KeyError:
    return HttpResponse("Invalid form!")
  else:
    new_time = parse_datetime(time_str)
    print(new_time)
    try:
      user = models.WechatUser.objects.get(pk=openid)
      reservations = models.Reservation.objects.filter(reserver=user)
      if len(reservations) > 0:
        reservation = reservations[0]
        return HttpResponse(
          "Reservation already exists: {}, Please type 'Cancel' in chat before making another reservation.".format(
            reservation))
      new_reservation = models.Reservation(reserver=user, arrival_time=new_time, guest_num=guest_num)
      new_reservation.save()

      async_send_message(user.get_id(),
                         "Reservation is confirmed for {} with {} guests at {}".format(user.get_nickname(),
                                                                                       new_reservation.get_guest_num(),
                                                                                       new_reservation.get_time()))
      return HttpResponse("Reservation {} has been made. Thank you!".format(new_reservation))
    except models.WechatUser.DoesNotExist:
      return HttpResponse("User not found!")


def api(request, model):
  from_time = request.GET.get('time')
  if model == models.Reservation.__name__ and from_time == 'fromNow':
    # TODO: Make sure options are are within the same day, or some way to distinguish them.
    now = timezone.now()
    incoming_quarter = ceil_dt(now)
    options = [incoming_quarter + datetime.timedelta(seconds=900 * i) for i in range(8)]
    # output = ["{}:{}".format(t.hour, t.min) for t in options]
    print(now, options)
    return HttpResponse(json.dumps(options, cls=DjangoJSONEncoder))
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
  if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
    print "valid request"
    echostr = request.GET.get('echostr')
    print request.body

    if echostr:
      return HttpResponse(echostr)
    else:
      # request.body contains the message xml
      msg = WechatData(request.body)
      process_msg(msg)
      return HttpResponse(" ")
  else:
    print "invalid request"
    return HttpResponse(status=406)


def get_reserve_url(msg):
  return "Please make a reservation at: http://wechat.grabbieteam.com/static/html/reserve.html?openid={}".format(
    msg.get_from_user_name())


def get_help_command():
  return textwrap.dedent("""\
  1: Make a reservation.
  2: Cancel an existing reservation.""")


def process_msg(msg):
  openid = msg.get_from_user_name()
  if msg.is_text_msg():
    if msg.get_content().lower() == 'cancel':
      try:
        user = models.WechatUser.objects.get(pk=openid)
      except models.WechatUser.DoesNotExist:
        print("user not found.")
      else:
        cancel_msg = "Reservation cancelled: "
        for r in user.reservation_set.all():
          cancel_msg = "{}{}".format(cancel_msg, r)
          r.delete()
        async_send_message(openid, cancel_msg)
    elif msg.is_subscribe_event():
      async_send_message(openid, get_reserve_url(msg))
    else:
      async_send_message(openid, get_reserve_url(msg))


def print_func(times):
  for i in range(times):
    print "hi there!"
    time.sleep(1)
