# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-09-09 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0007_auto_20180909_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(default='no-img.jpg', max_length=1024, upload_to='category/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='no-img.jpg', max_length=1024, upload_to='product/'),
        ),
    ]