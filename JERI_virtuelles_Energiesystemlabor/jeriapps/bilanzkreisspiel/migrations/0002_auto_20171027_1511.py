# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-27 15:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bilanzkreisspiel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='day',
            name='day_user',
        ),
        migrations.AddField(
            model_name='day',
            name='day_user',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
