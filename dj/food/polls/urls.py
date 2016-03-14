from pprint import pprint
from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from src.main.run import wechat
from . import models
from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^api/(?P<model>.+)', views.api, name='api'),
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
    else:
      reservation = models.Reservation(reserver=user, arrival_time=timezone.now(), guest_num=4)
      reservation.save()
      print "new:", reservation

print "starting up"

initialize()
