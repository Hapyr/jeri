# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from bilanzkreisspiel.models import *
from django.template.defaultfilters import default

class Lobby(models.Model):
    lobby_id = models.AutoField(primary_key=True)
    lobby_name = models.TextField()
    lobby_password = models.TextField()
    lobby_modus = models.TextField()
    
    def __unicode__(self):
        return self.lobby_name
   
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lobby = models.ForeignKey(Lobby, default='0', on_delete=models.CASCADE)
    
    # --- BilanzKreisSpieler Daten ---
    capital = models.IntegerField(default = 0)
    powerplantfleet = models.ForeignKey(PowerPlantFleet, default='0', on_delete=models.CASCADE)
    bks_status = models.BooleanField(default=False)
    bks_timeblock = models.ForeignKey(Timeblock, default='0', on_delete=models.CASCADE)
    #---Timeblock.objects.get(timeblock_number = -9999)
    
    # --- BörsenSpielSpieler Daten ---
    #---------------------------------
    def __unicode__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()