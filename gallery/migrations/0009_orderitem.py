# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-19 17:22
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0008_auto_20180909_1417'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('total_price', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.Product')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
