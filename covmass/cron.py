import schedule, time
from covmass.tasks import scrape

def cron():

  schedule.every().day.at("15:10").do(scrape)

  while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute
