from celery import Celery
from time import sleep

app = Celery("tasks", broker = "amqps://ovqqmupu:gIXxmO9EYYPg1khwmcInPD6yK7QUuboU@cow.rmq2.cloudamqp.com/ovqqmupu")

@app.task
def reverse(text):
    return text[::-1]