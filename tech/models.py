from django.db import models

# Create your models here.
class Tech(models.Model):
  name = models.CharField(max_length=60)

  def open_mic(self, venue):
    if venue.brand_id == 1 or not venue.building == 'park':
      return
