from __future__ import absolute_import, unicode_literals
from celery import shared_task
from time import sleep

@shared_task
def sleepy(duration):
  sleep(duration)
  print("wesh alors")
  return None

@shared_task
def newTest():
  Test.objects.create(name="nice")

@shared_task
def add(x, y):
  return x + y