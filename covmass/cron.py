from .models import Test

def my_scheduled_job():
  Test.objects.create(name="nice")
  
def hi():
  print("printed from crontab")
  f = open("/Users/gautier/Desktop/crontab.txt", "w")
  f.close()