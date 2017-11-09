import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from .models import brennstoffpreise,co2preise
from boersenspiel import fboersenspiel

def plotPreise():
    rohstoffe={'Kohle':1,'Gas':2,'Wasser':3}
    colors={1:"#CD853F",2:"#FFDAB9",3:"#0000FF"}
    for rohstoff in rohstoffe:
        preise=brennstoffpreise.objects.all().filter(idBrennstoff=rohstoffe[rohstoff],Runde__lte=fboersenspiel.gib_Runde()).order_by('Runde').values_list('Preis',flat=True)
        runde=brennstoffpreise.objects.all().filter(idBrennstoff=rohstoffe[rohstoff],Runde__lte=fboersenspiel.gib_Runde()).order_by('Runde').values_list('Runde',flat=True)
        plt.plot(runde,preise,'-o', c=colors[rohstoffe[rohstoff]])
        plt.xlabel('Runde')
        plt.ylabel('Preis [EUR/MWH]')
        plt.title(rohstoff+'preise')
        plt.axis([0,12,0,35])
        plt.grid(True)
        plt.savefig(os.path.dirname(__file__) + '/static/boersenspiel/images/tmp/'+rohstoff+'preise.png')
        plt.close() 
    
    
    preise=co2preise.objects.all().filter(Runde__lte=fboersenspiel.gib_Runde()).order_by('Runde').values_list('Preis',flat=True)
    runde=co2preise.objects.all().filter(Runde__lte=fboersenspiel.gib_Runde()).order_by('Runde').values_list('Runde',flat=True)
    plt.plot(runde,preise,'-o', c=colors[rohstoffe[rohstoff]])
    plt.xlabel('Runde')
    plt.ylabel('Preis [EUR/t]')
    plt.title('CO2-Preise')
    plt.axis([0,12,0,33])
    plt.grid(True)
    plt.savefig(os.path.dirname(__file__) + '/static/boersenspiel/images/tmp/Co2preise.png')
    plt.close()
          
    
    