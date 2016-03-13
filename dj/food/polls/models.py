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


class WechatUesr(models.Model):
  openid = models.CharField(max_length=200, primary_key=True)
  city = models.CharField(max_length=200)
  country = models.CharField(max_length=200)
  nickname = models.CharField(max_length=200)
  groupId = models.IntegerField(default=0)

  def from_json(self, json_data):
    self.openid = json_data['openid']
    self.city = json_data['city']
    self.country = json_data['country']
    self.groupid = json_data['groupid']
    self.nickname = json_data['nickname']

  def __str__(self):
    return self.nickname


class Reservation(models.Model):
  reserver = models.ForeignKey(WechatUesr)
  arrival_time = models.DateTimeField('ETA')
  guest_num = models.IntegerField(default=0)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return "{}, {}, {}".format(self.reserver, self.guest_num, self.arrival_time)