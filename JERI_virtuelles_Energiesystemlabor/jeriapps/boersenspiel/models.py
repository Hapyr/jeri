from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


# Create your models here.
class einstellungen(models.Model):
    Runde=models.IntegerField(default=0)
    idSpiel=models.IntegerField(default=1)
    auctiontype=models.IntegerField(default=1)
    nextround=models.DateTimeField(default=datetime.now, blank=True)
    rundenzeit=models.IntegerField(default=180)
    class Meta:
        verbose_name='Einstellungen'
        verbose_name_plural='Einstellungen'
            
class co2preise(models.Model):
    Runde=models.IntegerField(default=0)
    Preis=models.FloatField(default=0)
    class Meta:
        verbose_name='CO2 Preis'
        verbose_name_plural='CO2 Preise'
  
        
class brennstoffpreise(models.Model):
    idBrennstoff=models.IntegerField(default=0)
    Runde=models.IntegerField(default=0)
    Preis=models.FloatField(default=0)
    class Meta:
        verbose_name='Brennstoffpreis'
        verbose_name_plural='Brennstoffpeise'

class brennstoff(models.Model):
    id=models.IntegerField(default=0,primary_key=True)
    Name=models.CharField(max_length=30)
    EMF=models.FloatField(default=0)
    readonly_fields=('id',)
    class Meta:
        verbose_name='Brennstoff'
        verbose_name_plural='Brennstoffe'

class ergebnisse(models.Model):
    idSpiel=models.IntegerField(default=0)
    idSpieler=models.IntegerField(default=0)
    idRunde=models.IntegerField(default=0)
    erloes=models.IntegerField(default=0)
    kostenCo2=models.FloatField(default=0)
    kosten=models.FloatField(default=0)
    time=models.TimeField(default=datetime.now, blank=True)
    class Meta:
        verbose_name='Ergebnis'
        verbose_name_plural='Ergebnisse'
    
class boersenpreise(models.Model):
    runde=models.IntegerField(default=0)
    time=models.TimeField(default=datetime.now, blank=True)
    menge=models.IntegerField(default=0)
    preis=models.IntegerField(default=0)
    class Meta:
        verbose_name='Boersenpreis'
        verbose_name_plural='Boersenpreise'    
    
class lastgang(models.Model):
    idRunde=models.IntegerField(default=0)
    fMaxLast=models.FloatField(default=0)
    class Meta:
        verbose_name='Lastgang'
        verbose_name_plural='Lastgaenge'
        
class gebote(models.Model):
    idSpiel=models.IntegerField(default=0,null=True)
    idSpieler=models.IntegerField(default=0,null=True)
    Runde=models.IntegerField(default=0,null=True)
    idKW=models.IntegerField(default=0,null=True)
    idGebot=models.IntegerField(default=0,null=True)
    Time=models.TimeField(default=datetime.now, blank=True)
    Menge=models.IntegerField(default=0,null=True)
    Preis=models.IntegerField(default=0,null=True)
    class Meta:
        verbose_name='Gebot'
        verbose_name_plural='Gebote'
    
class kraftwerke(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=30)
    maxLeistung=models.IntegerField(default=0)
    verfuegbarkeit=models.FloatField(default=0)
    volllaststunden=models.IntegerField(default=0)
    idBrennstoff=models.IntegerField(default=0)
    wirkungsgrad=models.FloatField(default=0)
    fixkosten=models.FloatField(default=0)
    icon=models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        verbose_name='Kraftwerke'
        verbose_name_plural='Kraftwerke'
    
class spielerkraftwerke(models.Model):
    """Kraftwerke des jeweiligen Spielers"""
    id=models.IntegerField(primary_key=True)
    idSpiel=models.IntegerField(default=0)
    idSpieler=models.IntegerField(default=0,null=True)
    idKraftwerk=models.IntegerField(default=0)   
    verkaufteEnergiemenge=models.IntegerField(default=0)
    gewinn=models.FloatField(default=0)
    class Meta:
        verbose_name='SpielderKraftwerk'
        verbose_name_plural='SpielerKraftwerke'

class Spieler(models.Model):
    """
    DB der Spieler, bindet das Standart User-Model von Django ein um die Authentifizierung, Login und  Sessions von Django zu benutzen
    Weitere Felder: 
    Boersenspiel: isAdmin, idSpiel, Deckungsbeitrag
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    idSpieler=models.AutoField(primary_key=True)
    isAdmin=models.BooleanField(default=False)
    idSpiel=models.IntegerField(default=1)
    deckungsbeitrag=models.IntegerField(default=0)
    readonly_fields=('id',)
    class Meta:
        verbose_name='Spieler'
        verbose_name_plural='Spieler'    
    

@receiver(post_save, sender=User)
def create_user_spieler(sender, instance, created, **kwargs):
    """Erstellung eines Users, erstellt auch das entsprechende Spieler Object """
    if created:
        spieler= Spieler.objects.create(user=instance)
        spieler.save()
        for kw in range(1,4):
            spielerkraftwerke.objects.create(idSpiel=spieler.idSpiel, idSpieler=spieler.idSpieler,idKraftwerk=kw)
            for bid in range (1,5):
                gebote.objects.create(idSpiel=spieler.idSpiel,idSpieler=spieler.idSpieler,Runde=einstellungen.objects.get().Runde,idKW=kw,idGebot=bid)
        

@receiver(post_save, sender=User)
def save_user_spieler(sender, instance, **kwargs):
    """Updates des User-Models updatet auch das Spieler Object"""
    instance.spieler.save()
    
      

    