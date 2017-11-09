""""Erstellt den HTML-Content fuer die Handler Seite"""
from boersenspiel import fboersenspiel as fb
from .models import gebote, kraftwerke,spielerkraftwerke


def init_KraftwerksDiv(request):
    """"Holt fuer den User im request die Gebote pro Kraftwerksblock fuer die aktuelle Runde aus der Datenbank
        und ruft mit ihnen gib_KraftwerksDiv auf"""
    preise=gebote.objects.filter(idSpiel=fb.gib_Spiel(request),Runde=fb.gib_Runde(),idSpieler=fb.gib_Spieler(request)).order_by('idKW','idGebot')
    return gib_KraftwerksDiv(request, preise)

def gib_KraftwerksDiv(request, preise):
    """Erhaelt Gebote pro Block und gibt html string zurueck
    """
    """Hole Preise aus der DB fuer KWs und Bloecke"""
    preise=preise.values_list()
    

    html=""
    html+='<td><table>'\
    + getKraftwerksdaten(request,1) +'</table></td><td class="noframe spacer"></td><td><table>'\
    + getKraftwerksdaten(request,2) +'</table></td><td class="noframe spacer"></td><td><table>'\
    + getKraftwerksdaten(request,3) +'</table></td>'
    return html

def getKraftwerksdaten(request,idKW):
    """Berechne Parameter/Variablen aus DB ziehen"""
    verkaufteMenge=spielerkraftwerke.objects.get(idSpieler=fb.gib_Spieler(request),idKraftwerk=idKW).verkaufteEnergiemenge
    vollLastStunden=kraftwerke.objects.get(id=idKW).volllaststunden
    maxLeistung=kraftwerke.objects.get(id=idKW).maxLeistung
    energieRest=99999
    blockLeistung=maxLeistung/4
    """ Kraftwerks Infos HTML"""
    
    html="<p class='ueberschirft'>"+kraftwerke.objects.get(id=idKW).name+"</p><table><tr><td>Max. Power:</td><td> " + str(maxLeistung) + " MW <br />"\
    "(4 * "+str(blockLeistung)+"MW)</td></tr><tr><td>Efficiency:</td><td> "+ str(kraftwerke.objects.get(id=idKW).wirkungsgrad*100)+ "%</td></tr>"\
    "<tr><td>Sold: </td><td>" + str(verkaufteMenge)+"</td></tr>"\
    "<tr><td>CM1: </td><td>"+ str(spielerkraftwerke.objects.get(idSpieler=fb.gib_Spieler(request),idKraftwerk=idKW).gewinn) + "</td></tr>"

    """Berechnung des Wasserkraftwerks"""
    if vollLastStunden>0:
        energieRest=vollLastStunden*maxLeistung-verkaufteMenge
    if vollLastStunden>0:
        if energieRest<0:
            html+="<tr><td>Energy left:</td><td><b>" + str(energieRest) + ' MWh </b></td></tr>'
        else:
            html+="<tr><td>Energy left:</td><td><b>" + str(energieRest) + ' MWh </b></td></tr>'
    
    
    """Eingabe des Preises HTML"""
    #blocks=["A", "B", "C", "D"]
    #for block in blocks:
    #    if energieRest>blockLeistung:
    #        energieRest=energieRest-blockLeistung
    #        html+='<tr><td> Leistung Block <b>' + block + '</td><td>'+str(blockLeistung)+' MW </b></td></tr>'
    #    else:
    #        html+='<tr><td> Leistung Block <b>' + block + '</td><td> 0 MW </b></td></tr>'
    return html
