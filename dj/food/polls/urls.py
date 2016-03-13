from django.conf.urls import url
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from . import models

from . import views
from pprint import pprint
urlpatterns = [
    url(r'^$', views.index, name='index'),
]


def initialize():
  user_ids = ["odIgav434SsjB4x8ROU7BJWzI5IU", "odIgav6fGLauJA1ukAtV_lGWWCPY", "odIgavz5qd3QrLSHyK5nefTgyIH4"]
  for user_id in user_ids:
    # user = user_manager.process_new_user(user_id)
    # pprint(user)
    try:
      existing_user = models.WechatUesr.objects.get(pk=user_id)
      print "existing: "
      pprint(existing_user)
    except ObjectDoesNotExist:
      x = models.WechatUesr()
      x.from_json(wechat.get_user_info(user_id))
      x.save()
      print "new: "
      pprint(x)



    # x = serializers.deserialize("json", user)
    # print x
    # break
    # db.user.save(user)


print "starting up"
from src.main.server import *
initialize()