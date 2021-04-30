from django.core.management.base import BaseCommand, CommandError
from covmass.cron import cron

class Command(BaseCommand):
  help = 'Scrapes web pages'

  def add_arguments(self, parser):
    parser.add_argument('moment', type=str) # argument with format hh:mm

  def handle(self, *args, **options):
    return cron(moment=options["moment"])
