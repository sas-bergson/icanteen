# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-04-30 09:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0003_remove_customer_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='state_province',
        ),
    ]
