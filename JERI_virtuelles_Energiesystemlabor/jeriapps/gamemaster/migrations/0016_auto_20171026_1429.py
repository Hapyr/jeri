# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-26 14:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gamemaster', '0015_auto_20171026_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='powerplantfleet',
            field=models.OneToOneField(default='0', on_delete=django.db.models.deletion.CASCADE, to='bilanzkreisspiel.PowerPlantFleet'),
        ),
    ]
