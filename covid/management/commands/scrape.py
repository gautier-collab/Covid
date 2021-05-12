from django.core.management.base import BaseCommand, CommandError
from covid.cron import cron

class Command(BaseCommand):
  help = 'Scrapes web pages'

  def add_arguments(self, parser):
    parser.add_argument('hour', type=str)
    parser.add_argument('minute', type=str)
    
  def handle(self, *args, **options):
    return cron(hour=options["hour"], minute=options["minute"])
