# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-30 09:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0012_auto_20190126_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=1024, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='gallery.Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='designation',
            field=models.CharField(db_index=True, max_length=1024, unique=True),
        ),
    ]