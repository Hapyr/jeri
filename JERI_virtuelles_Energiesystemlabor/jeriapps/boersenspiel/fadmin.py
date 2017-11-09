"""HTML-Code und Funktionen der Adminseite"""
from django.contrib import messages
from boersenspiel.models import spielerkraftwerke, gebote, boersenpreise, ergebnisse , User,\
    einstellungen, brennstoffpreise, lastgang,  brennstoff, co2preise, Spieler, datetime, kraftwerke
from boersenspiel import fboersenspiel as fb, fmarkets
import csv
import os
#from datetime import datetime
from datetime import timedelta
from boersenspiel.fboersenspiel import gib_Runde
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

def reset(request,mode):
    """Mode:1 Loescht auch Spieler sonst nur Gebote und Kraftwerke und initiert fuer alle Spieler diese neu"""
    try:
        if mode==1:
            userList=User.objects.all().filter(is_staff=False)
            userList.delete()
            messages.success(request, 'All non Staffmembers are deleted.')
        spielerkraftwerke.objects.filter().delete()
        messages.success(request, 'All Spielerkraftwerke are deleted.')        
        gebote.objects.filter().delete()
        messages.success(request, 'All Spieler Gebote are deleted.')
        ein=einstellungen.objects.get()
        ein.Runde=1
        ein.save()
        boersenpreise.objects.filter().delete()    
        messages.success(request, 'All Boersenspreise are deleted.')
        ergebnisse.objects.filter().delete()
        messages.success(request, 'All Ergebnissee are deleted.')
        userList=User.objects.all()
        for user in userList:
            fb.initSpieler(user.spieler)
    except Exception as e:
        messages.error(request, e)

    """Loesche Bilder im Ordner tmp"""
    folder = os.path.dirname(__file__)+'/static/boersenspiel/images/tmp'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
    """Plotte leere Boersenspreise"""      
    plotBoersenpreis([0,],[0,])
    """Plotte Brennstoffpreise neu"""
    fmarkets.plotPreise()

def ladedaten():
    """Laed die Brennstoffpreise,Lastgang CO2Preise und Brennstoffe neu"""
    brennstoffpreise.objects.all().delete()
    reader=csv.reader(open(os.path.dirname(__file__) + "/static/boersenspiel/data/brennstoffpreise.csv"))
    for row in reader:
        brennstoffpreise.objects.create(idBrennstoff=row[0], Runde=int(row[1]), Preis=int(row[2]))
        
    lastgang.objects.all().delete()
    reader=csv.reader(open(os.path.dirname(__file__) + "/static/boersenspiel/data/lastgang.csv"))
    for row in reader:
        lastgang.objects.create(idRunde=row[0], fMaxLast=float(row[1]))        
    
    brennstoff.objects.all().delete()
    reader=csv.reader(open(os.path.dirname(__file__) + "/static/boersenspiel/data/brennstoff.csv"))
    for row in reader:
        brennstoff.objects.create(id=row[0],Name=row[1], EMF=float(row[2])) 
   
    co2preise.objects.all().delete()
    reader=csv.reader(open(os.path.dirname(__file__) + "/static/boersenspiel/data/co2preise.csv"))
    for row in reader:
        co2preise.objects.create(Runde=row[0],Preis=float(row[1]))

def neueRunde():
    #TODO auktion
    
    #Erhoehe Runde
    einstellungenquery=einstellungen.objects.get()
    einstellungenquery.Runde+=1
    #Setze Endzeit der Runde auf jetzt + rundenzeit
    einstellungenquery.nextround=datetime.now()+timedelta(seconds=einstellungenquery.rundenzeit)
    einstellungenquery.save()
    #PLotte Grafiken fuer neue Runde
    fmarkets.plotPreise()
    
def plotBoersenpreis(runde,preise):
    plt.plot(runde,preise,'-o')
    plt.xlabel('Runde')
    plt.ylabel('Preis [EUR/MWh]')
    plt.title('Boersenpreise')
    plt.axis([0,12,0,200])
    plt.grid(True)
    plt.savefig(os.path.dirname(__file__) + '/static/boersenspiel/images/tmp/Boersenpreise.png')
    plt.close()
    
def plotMeritOrder(mcp,mcv,data,name):
    """ mcp=Market Clearing Price,
        mcv=Market Clearing Value,
        data=Liste mit Preis und Menge
        name=Spielername oder Alles"""
    preis=data.values_list('Preis',flat=True)
    menge=data.values_list('Menge',flat=True)
    ypos=0
    for preis,menge in data:
        if preis<mcp:
            farbe="green"
        if preis==mcp:
            farbe="yellow"
        if (preis>=mcp) and (ypos>=mcv):
            farbe="red"
            
        plt.bar(ypos,preis,menge,align="edge",alpha=0.5,edgecolor="grey",color=farbe)
        ypos+=menge
    plt.xlabel('Energie [MWh]')
    plt.ylabel('Preis [EUR/MWh]')
    plt.title('Merit Order Runde:'+str(gib_Runde()))
    plt.axhline(mcp)
    plt.axvline(mcv)
    plt.annotate('MCP='+str(mcp)+'Euro/MWh',xy=(1,mcp+5))
    plt.annotate('MCV='+str(mcv)+'MWh',xy=(mcv+5,mcp+5))
    plt.savefig(os.path.dirname(__file__) + '/static/boersenspiel/images/tmp/'+name+'MeritOrder'+str(gib_Runde())+'.png')
    plt.close()
    
def auktion():
    """Berechne Last (Maximale Leistung im Spiel*Lastfaktor)"""
    """Berechne Maximale Leistung"""
    numSpieler=Spieler.objects.all().count()
    maxLeistung=numSpieler*(kraftwerke.objects.get(id=1).maxLeistung)
    maxLeistung+=numSpieler*(kraftwerke.objects.get(id=2).maxLeistung)
    maxLeistung+=numSpieler*(kraftwerke.objects.get(id=3).maxLeistung)
    """Lastfaktor"""
    lastfaktor=lastgang.objects.get(idRunde=gib_Runde()).fMaxLast
    last=maxLeistung*lastfaktor
    """Berechne Marktpreis mcp"""
    handelsmenge=0
    mcp=0
    angebotsliste=gebote.objects.all().filter(Runde=gib_Runde()).order_by('Preis','Time','idGebot').values_list('Preis','Menge')
    for preis, menge in angebotsliste:
        if handelsmenge<last:
            if handelsmenge+menge > last:
                menge=last-handelsmenge
            handelsmenge+=menge
            mcp=preis
        else:break    
    obj, created=boersenpreise.objects.update_or_create(defaults={'time':datetime.now(),'menge':handelsmenge,'preis':mcp},runde=gib_Runde())
    

    
    """Plotte Boersenpreisverlauf""" 
    runde=boersenpreise.objects.all().order_by('runde').values_list('runde',flat=True)
    preise=boersenpreise.objects.all().order_by('runde').values_list('preis',flat=True)
    plotBoersenpreis(runde, preise)

    """Plotte MeritOrder fuer alle Angebote"""
    angebotsliste=gebote.objects.all().filter(Runde=gib_Runde()).order_by('Preis','Time','idGebot').values_list('Preis','Menge')
    plotMeritOrder(mcp, handelsmenge, angebotsliste,'Gesamt')
    
    """Berechne Erloese,Gewinne und Kosten"""
    handelsmenge2=0
    angebotsliste=gebote.objects.all().filter(Runde=gib_Runde()).order_by('Preis','Time','idGebot').values_list('Preis','Menge','idSpieler','idKW')
    for preis, menge, spieler, kw in angebotsliste: 
        diff=preis-boersenpreise.objects.get(runde=gib_Runde()).preis
        if diff<0:
            diff=0
        """Hole Wirkungsgrad n, Emissionsfaktor EMF und Brennstoffpreis brennpreis"""
        n=kraftwerke.objects.get(id=kw).wirkungsgrad
        emf=brennstoff.objects.get(id=kw).EMF
        brennpreis=brennstoffpreise.objects.get(idBrennstoff=kw,Runde=gib_Runde()).Preis
        """CO2 Preis"""
        co2preis=co2preise.objects.get(Runde=gib_Runde()).Preis
        """Erloese und Kosten und Kosten Co2"""
        erloes=0
        kosten=0
        kosten_co2=0
        """Beginne Berechnung"""
        if handelsmenge2<handelsmenge:
            if handelsmenge2+menge>handelsmenge:
                menge=handelsmenge-handelsmenge2
            if einstellungen.objects.get().auctiontype is 1:
                erloes=menge*preis
                kosten=(menge/n)*(brennpreis+(emf*co2preis))
                kosten_co2=(menge/n)*(emf*co2preis) 
            elif einstellungen.objects.get().auctiontype is 2:
                erloes=menge*mcp
                kosten=(menge/n)*(brennpreis+(emf*co2preis))
                kosten_co2=(menge/n)*(emf*co2preis)   
            gewinn=erloes-kosten    
            """Speicher Ergebnisse""" 
            ergebniss, created=ergebnisse.objects.get_or_create(idSpieler=spieler,idRunde=gib_Runde())
            ergebniss.erloes+=erloes
            ergebniss.kosten+=kosten
            ergebniss.kostenCo2+=kosten_co2
            ergebniss.time=datetime.now()
            ergebniss.save()
            """Speicher Gewinne und Verkaufte Mengen"""
            kwupdate=spielerkraftwerke.objects.get(idSpieler=spieler,idKraftwerk=kw)
            kwupdate.gewinn+=gewinn
            kwupdate.verkaufteEnergiemenge+=menge
            kwupdate.save()
            
        handelsmenge2+=menge                  
    for spieler in Spieler.objects.all():
            plotMeritOrder(mcp, handelsmenge, gebote.objects.filter(idSpieler=spieler.user.pk,Runde=gib_Runde()).order_by('Preis','Time','idGebot').values_list('Preis','Menge'), spieler.user.username)
            
        