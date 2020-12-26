from __future__ import unicode_literals

from django.db import models

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    amount = models.CharField(max_length=10)
    tel = models.CharField(max_length=13)
    payment_date = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    class Meta: #meta class for ordering orders based on date created
        ordering = ('-payment_date', )

    def __str__(self):
        return 'Payment {}'.format(self.id)




#create your models here
