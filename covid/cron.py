import schedule, time
from covid.tasks import scrape
from selenium import webdriver

def cron(hour, minute):

  # DEVELOPMENT MODE CONFIGURATION
  PATH="/Users/gautier/Documents/Z/Chromedriver/chromedriver"
  driver = webdriver.Chrome(PATH)

  # PRODUCTION MODE CONFIGURATION (FOR VIRTUAL MACHINE)
  #PATH=f"{settings.BASE_DIR}/staticfiles/chromedriver"
  #user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
  #options = webdriver.ChromeOptions()
  #options.headless = True
  #options.add_argument(f'user-agent={user_agent}')
  #options.add_argument("--window-size=1920,1080")
  #options.add_argument('--ignore-certificate-errors')
  #options.add_argument('--allow-running-insecure-content')
  #options.add_argument("--disable-extensions")
  #options.add_argument("--proxy-server='direct://'")
  #options.add_argument("--proxy-bypass-list=*")
  #options.add_argument("--start-maximized")
  #options.add_argument('--disable-gpu')
  #options.add_argument('--disable-dev-shm-usage')
  #options.add_argument('--no-sandbox')
  #driver = webdriver.Chrome(PATH, options=options)


  #schedule.every().day.at(f"{hour}:{minute}").do(scrape, driver)

  #while True:
  #  schedule.run_pending()
  #  time.sleep(60) # wait one minute


  # Execute immediately for test:
  scrape(driver)