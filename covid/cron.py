import schedule, time
from covid.tasks import scrape

def cron(hour, minute):

  schedule.every().day.at(f"{hour}:{minute}").do(scrape)

  while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute

  # # Execute immediately for test:
  # scrape()