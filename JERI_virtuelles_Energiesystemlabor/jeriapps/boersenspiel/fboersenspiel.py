""""Allgemeine Funktionen zum Boersenspiel"""
from .models import spielerkraftwerke, einstellungen, Spieler

def gib_Spieler(request):
    return Spieler.objects.get(user=request.user).idSpieler
    
def gib_Runde():
    return einstellungen.objects.get().Runde

def gib_Spiel(request):
    return Spieler.objects.get(user=request.user).idSpiel
    
def initSpieler(player):
    for kw in range(1,4):
        spielerkraftwerke.objects.create(idSpiel=player.idSpiel, idSpieler=player.idSpieler,idKraftwerk=kw,)
        #for bid in range (1,5):
        #   gebote.objects.create(idSpiel=player.idSpiel,idSpieler=player.idSpieler,Runde=fboersenspiel.gib_Runde(),idKW=kw,idGebot=bid,Menge=kraftwerke.objects.get(id=kw).maxLeistung/4)


    