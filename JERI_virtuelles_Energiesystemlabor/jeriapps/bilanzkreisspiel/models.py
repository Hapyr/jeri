# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Day(models.Model):
    day_id = models.AutoField(primary_key=True)
    day_user = models.ForeignKey(User,default='0')
    day_number = models.IntegerField()
    
    def __unicode__(self):
        return str(self.day_id)
    
class Timeblock(models.Model):
    timeblock_id = models.AutoField(primary_key=True)
    timeblock_day = models.ForeignKey(Day,default='0')
    timeblock_number = models.IntegerField()
    timeblock_duration = models.IntegerField()
    
    def __unicode__(self):
        return str(self.timeblock_id)
    
class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.TextField()
    event_discription = models.TextField()
    event_from_timeblock = models.ManyToManyField(Timeblock)
    event_duration = models.IntegerField()
    event_feed_in = models.IntegerField()
    event_feed_out = models.IntegerField()
    
    def __unicode__(self):
        return self.event_name
    
class PowerPlantFleet(models.Model):
    powerplantfleet_id = models.AutoField(primary_key=True)
    powerplantfleet_name = models.TextField()

    def __unicode__(self):
        return self.powerplantfleet_name
    
class PowerStation(models.Model):
    powerstation_id = models.AutoField(primary_key=True)
    powerstation_name = models.TextField()
    powerstation_current_feed_in = models.IntegerField()
    powerstation_current_feet_out = models.IntegerField()
    powerstation_powerplantfleet = models.ManyToManyField(PowerPlantFleet)
    
    def __unicode__(self):
        return self.powerstation_name
    
     