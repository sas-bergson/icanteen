# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-09-05 02:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_auto_20180905_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=1024, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='path_to_picture',
            field=models.CharField(blank=True, max_length=4096),
        ),
        migrations.AlterField(
            model_name='product',
            name='designation',
            field=models.CharField(max_length=1024, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='packaging',
            field=models.CharField(max_length=4096),
        ),
        migrations.AlterField(
            model_name='product',
            name='path_to_picture',
            field=models.CharField(max_length=4096, unique=True),
        ),
    ]
