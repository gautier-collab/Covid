from django.db import models
from django.db.models.signals import post_save

class Source(models.Model):
  name = models.CharField(max_length=32)
  url = models.CharField(max_length=128)

  def __str__(self):
    return self.name


class Zone(models.Model):
  name = models.CharField(max_length=32)
  source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="zones")
  # infected = models.ForeignKey(Infected, on_delete=models.CASCADE, related_name="zone", null=True)
  # deaths = models.ForeignKey(Deceased, on_delete=models.CASCADE, related_name="zone", null=True)

  def __str__(self):
    return self.name

class Metric(models.Model):
  total = models.IntegerField()
  # total_per_hour = models.CharField(max_length=1024)
  new = models.IntegerField()

class Infected(Metric):
  zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="infected")

class Deceased(Metric):
  zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="deceased")
