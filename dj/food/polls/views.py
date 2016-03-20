import json
import time
from threading import Thread
from src.main.run import wechat
from src.main.server import WechatData
from pprint import pprint
from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from django.views.decorators.http import require_http_methods
from . import models

def index(request):
  return HttpResponse("Hello, world. You're at the polls index.")
  # return render(request, 'hello.html')

def api(request, model):
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
  pprint(request.body)
  if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
    print "valid request"
    echostr = request.GET.get('echostr')
    if echostr:
      return HttpResponse(echostr)
    else:
      # request.body contains the message xml
      msg = WechatData(request.body)
      if msg.is_text_msg():
        t = Thread(target=send_message, args=(msg.get_from_user_name(), "hello there, fool"))
        t.start()
      return HttpResponse(" ")
  else:
    print "invalid request"
    return HttpResponse(status=406) 

def print_func(times):
  for i in range(times):
    print "hi there!"
    time.sleep(1)

def send_message(username, content):
  wechat.send_text_message(username, "hello there, fool")
