from django.db import models

# Create your models here.
class Genre(models.Model):
  name = models.CharField(max_length=127)
  year_invented = models.PositiveSmallIntegerField()
  
  def __str__(self):
    return self.name
    
  @property
  def display_attrs(self):
    return {"name": self.name}