import json

from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers

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