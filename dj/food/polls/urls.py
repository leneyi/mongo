from threading import Thread

import time

import math
from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from polls.util import async_send_message
from src.main.run import wechat
from . import models
from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^verify', views.verify, name='verify'),
  url(r'^api/(?P<model>.+)', views.api, name='api'),
  url(r'^reserve', views.reserve, name='reserve'),
]


def initialize():
  # Initialize users
  user_ids = ["odIgav434SsjB4x8ROU7BJWzI5IU", "odIgav6fGLauJA1ukAtV_lGWWCPY", "odIgavz5qd3QrLSHyK5nefTgyIH4"]
  for user_id in user_ids:
    # user = user_manager.process_new_user(user_id)
    # pprint(user)
    try:
      existing_user = models.WechatUser.objects.get(pk=user_id)
      print "existing: ", existing_user
    except ObjectDoesNotExist:
      new_user = models.WechatUser()
      new_user.from_json(wechat.get_user_info(user_id))
      new_user.save()
      print "new: ", new_user

  # Make up reservations
  for user in models.WechatUser.objects.all():
    reservation = models.Reservation.objects.filter(reserver=user.openid)
    if reservation:
      print "existing: ", reservation
      # reservation.delete()
    # else:
    #   reservation = models.Reservation(reserver=user, arrival_time=timezone.now(), guest_num=4)
    #   reservation.save()
    #   print "new:", reservation

def reminder_job():
  def calculate_time_left(reservation):
    left = reservation.get_time() - timezone.now()
    print(reservation.get_time(), timezone.now())
    return left.total_seconds()

  while True:
    for r in models.Reservation.objects.all():
      seconds_left = calculate_time_left(r)
      reminder_message = "{} min left".format(int(seconds_left/60))
      print(reminder_message)
      if seconds_left < 0:
        print("Expired. Delete.", r)
        r.delete()
      elif seconds_left < 1500:
        async_send_message(r.get_reserver().get_id(), reminder_message)

    print("sleep..")
    time.sleep(60)

def launch_reminder_job():
  t = Thread(target=reminder_job, args=())
  t.start()



print("starting up")
initialize()
launch_reminder_job()