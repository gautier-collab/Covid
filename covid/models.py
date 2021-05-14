from django.db import models
from django.db.models.signals import post_save

class Source(models.Model):
  name = models.CharField(max_length=32)
  url = models.CharField(max_length=128)

  def __str__(self):
    return self.name


class Zone(models.Model):
  name = models.CharField(max_length=32)
  german_name = models.CharField(max_length=32, null=True)
  source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="zones")
  # infected = models.ForeignKey(Infected, on_delete=models.CASCADE, related_name="zone", null=True)
  # deaths = models.ForeignKey(Deceased, on_delete=models.CASCADE, related_name="zone", null=True)

  def __str__(self):
    return self.name

class Metric(models.Model):
  # total_per_hour = models.CharField(max_length=1024)
  total = models.IntegerField()
  new = models.IntegerField()
  update = models.DateTimeField(auto_now=True, null=True)

  def display_total(self):
    return "{:,}".format(self.total).replace(",", "'")

  def display_new(self):
    return "{:,}".format(self.new).replace(",", "'")

class Infected(Metric):
  zone = models.OneToOneField(Zone, on_delete=models.CASCADE, related_name="infected")

  def __str__(self):
    return f"{self.zone.name} inf."

class Deceased(Metric):
  zone = models.OneToOneField(Zone, on_delete=models.CASCADE, related_name="deceased")

  def __str__(self):
    return f"{self.zone.name} deaths"
  
class Update(models.Model):
  time = models.CharField(max_length=64)
  
  def __str__(self):
    return self.time
  
class Zurich_update(models.Model):
  time = models.CharField(max_length=64)
  display = models.BooleanField(default=False)