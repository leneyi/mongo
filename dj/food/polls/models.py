from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class Question(models.Model):
  question_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')

  def was_published_recently(self):
    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

  def __str__(self):
    return self.question_text


class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)
  votes = models.IntegerField(default=0)

  def __str__(self):
    return self.choice_text


class Status(object):
  INIT = 10
  ASK_FOR_TIME = 20
  CONFIRMED = 30
  CANCELLED = 40


class WechatUser(models.Model):
  openid = models.CharField(max_length=200, primary_key=True)
  city = models.CharField(max_length=200)
  country = models.CharField(max_length=200)
  nickname = models.CharField(max_length=200)
  groupId = models.IntegerField(default=0)
  msg_state = models.IntegerField(default=Status.INIT)

  def from_json(self, json_data):
    self.openid = json_data['openid']
    self.city = json_data['city']
    self.country = json_data['country']
    self.groupid = json_data['groupid']
    self.nickname = json_data['nickname']

  def __str__(self):
    return self.nickname

  def get_state(self):
    return self.msg_state

  def get_id(self):
    return self.openid


# class UserState(models.Model):
#   user = models.ForeignKey(WechatUser)
#   timestamp = models.DateTimeField(auto_now_add=True)
#   content = models.CharField(max_length=200)
#   status = models.IntegerField(default=Status.INIT)
#

class Reservation(models.Model):
  reserver = models.ForeignKey(WechatUser)
  arrival_time = models.DateTimeField('ETA')
  guest_num = models.IntegerField(default=0)
  created = models.DateTimeField(auto_now_add=True)

  def get_guest_num(self):
    return self.guest_num

  def get_time(self):
    return self.arrival_time

  def __str__(self):
    return "{}, {}, {}".format(self.reserver, self.guest_num, self.arrival_time)