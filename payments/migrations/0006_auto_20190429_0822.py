# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-04-29 08:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_auto_20190429_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='tel',
            field=models.CharField(max_length=13),
        ),
    ]
