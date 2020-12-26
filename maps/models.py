from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    description = models.TextField(max_length=1000)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    def _str_(self):
        return self.name




