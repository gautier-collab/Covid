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