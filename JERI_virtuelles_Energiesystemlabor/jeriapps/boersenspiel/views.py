from django.shortcuts import render,redirect
from django.http.response import Http404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout 
from boersenspiel import fhandler as fh, fboersenspiel as fb, fadmin,\
    fboersenspiel
from django.contrib.auth.forms import UserCreationForm
from boersenspiel.forms import bidscoal,bidswater,bidsgas,  einstellungenForm
from boersenspiel.models import gebote,einstellungen, Spieler, spielerkraftwerke, kraftwerke
from boersenspiel.fboersenspiel import gib_Runde

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return handler(request)
    else:
        form = UserCreationForm()
    return render(request, 'boersenspiel/signup.html', {'form': form, 'runde':fboersenspiel.gib_Runde()})

def handler(request):
    
    if  not request.user.is_authenticated():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return handler(request)
            else:
                return redirect('login')
    else:
        formcoal=bidscoal(request.POST)
        formgas=bidsgas(request.POST)
        formwater=bidswater(request.POST)
        if formcoal.is_valid():
            for bid in range(1,5):
                gebotequery, created=gebote.objects.get_or_create(idSpieler=fb.gib_Spieler(request),idKW=1,idGebot=bid,Runde=gib_Runde(),Menge=kraftwerke.objects.get(id=1).maxLeistung/4)
                gebotequery.Preis=request.POST['kw1'+str(bid)]
                gebotequery.save()   
        else:
            formcoal=bidscoal() 
             
        if formgas.is_valid():
            for bid in range(1,5):
                gebotequery, created =gebote.objects.get_or_create(idSpieler=fb.gib_Spieler(request),idKW=2,idGebot=bid,Runde=gib_Runde(),Menge=kraftwerke.objects.get(id=2).maxLeistung/4)
                gebotequery.Preis=request.POST['kw2'+str(bid)]
                gebotequery.save()   
        else:
            formgas=bidsgas()
        if formwater.is_valid():
            for bid in range(1,5):
                gebotequery, created=gebote.objects.get_or_create(idSpieler=fb.gib_Spieler(request),idKW=3,idGebot=bid,Runde=gib_Runde(),Menge=kraftwerke.objects.get(id=3).maxLeistung/4)
                gebotequery.Preis=request.POST['kw3'+str(bid)]
                gebotequery.save()   
        else:
            formwater=bidswater()            
                              
    return render(request, 'boersenspiel/handler.html',{'html':fh.init_KraftwerksDiv(request),'formcoal':formcoal,'formwater':formwater, 'formgas':formgas, 'runde':fboersenspiel.gib_Runde()})

def login(request):
    return render(request, 'boersenspiel/login.html',{'runde':fboersenspiel.gib_Runde()})

def logout(request):
    auth_logout(request)
    return redirect('login')

def admin(request):
    if request.user.is_staff:
        if(request.GET.get('resetGame')):
            fadmin.reset(request,0)
        if(request.GET.get('resetAll')):
            fadmin.reset(request,1)
        if(request.GET.get('lade')):
            fadmin.ladedaten()
        if(request.GET.get('neueRunde')):
            fadmin.neueRunde()
        if(request.GET.get('auktion')):
            fadmin.auktion()           
        return render(request, 'boersenspiel/admin.html',{'runde':fboersenspiel.gib_Runde()})
    else:
        return redirect('login')
    raise Http404

def prefs(request):
    form=einstellungenForm(request.POST)
    if form.is_valid():
            einstellungquery=einstellungen.objects.get()
            einstellungquery.Runde=request.POST['Runde']
            einstellungquery.idSpiel=request.POST['Spiel']
            einstellungquery.auctiontype=request.POST['auctiontype']
            einstellungquery.nextround=request.POST['nextround']
            einstellungquery.rundenzeit=request.POST['rundenzeit']
            einstellungquery.save()
    else:
        form=einstellungenForm()
    return render(request,'boersenspiel/prefs.html',{'form':form, 'runde':fboersenspiel.gib_Runde()})

def externalmarkets(request):
    return render(request,'boersenspiel/markets.html',{'runde':fboersenspiel.gib_Runde()})

def highscores(request):
    data=[]
    spielerListe=Spieler.objects.all()
    for spieler in spielerListe:
        name=spieler.user.username
        gewinn=0.0
        for x in range(1,4):
            gewinn+=spielerkraftwerke.objects.get(idSpieler=spieler.pk,idKraftwerk=x).gewinn
        data=data+[(name,gewinn)]
    data.sort(key=lambda tup:tup[1],reverse=True)
    return render(request,'boersenspiel/hs.html',{'liste':data, 'runde':fboersenspiel.gib_Runde()})

def auctionsresults(request):
    dataGesamt=[]
    dataSpieler=[]
    
    for i in range(1,gib_Runde()+1):
        dataGesamt.append('boersenspiel/images/tmp/GesamtMeritOrder'+str(i)+'.png') 
    dataGesamt.reverse()    
    for j in range(1,gib_Runde()+1):
        dataSpieler.append('boersenspiel/images/tmp/PhenMeritOrder'+str(j)+'.png')
    dataSpieler.reverse()
    
        
    return render(request,'boersenspiel/results.html',{'runde':fboersenspiel.gib_Runde(),'gesamt':dataGesamt,'spieler':dataSpieler})
