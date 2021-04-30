import schedule, time
from covmass.tasks import scrape

def cron(moment):

  schedule.every().day.at(moment).do(scrape)

  while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute
