# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-20 15:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamemaster', '0007_gamer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gamer',
            old_name='gamer_lobbyid',
            new_name='lobby_id',
        ),
    ]