from django.core.management.base import BaseCommand, CommandError
from covmass.cron import cron

class Command(BaseCommand):
  help = 'Scrapes web pages'

  # def add_arguments(self, parser):
  #   parser.add_argument('duration', type=int)

  def handle(self, *args, **options):
    # return scrape(duration=options["duration"])
    return cron()
