# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.template.context_processors import request
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from bilanzkreisspiel.models import *
from gamemaster.models import *
from gamemaster.forms import *  
from gamemaster import *

from bilanzkreisspiel.init_data import DURATION_PER_DAY
from bilanzkreisspiel.init_data import NUMBER_DAYS
from bilanzkreisspiel.init_data import NUMBER_TIMEBLOCKS

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.staticfiles.templatetags.staticfiles import static


def gamestart(request):
    gamer = request.user.profile
    if request.user.is_authenticated():
        if gamer.bks_status==False: # --- First time playing this game --- 
            init_game(request)   
            gamer.bks_status=1
            gamer.bks_timeblock=Timeblock.objects.get(timeblock_day=Day.objects.get(day_user=request.user,day_number=0), timeblock_number=0);
            gamer.save()
                     
        
        if request.method == 'POST':    
            if request.POST.get('next')=='Next Round':
                setNextTimeblock(request)
            elif request.POST.get('next')=='Next Day':
                setNextDay(request)
            elif request.POST.get('next')=='Reset':
                init_reset(request)
                init_game(request)
                
            gamer.save()   
            gamer.save()                 
            
            mname = request.user.username
            timebs = Timeblock.objects.raw('SELECT bilanzkreisspiel_timeblock.timeblock_id FROM (auth_user INNER JOIN bilanzkreisspiel_day ON auth_user.id = bilanzkreisspiel_day.day_user_id) INNER JOIN bilanzkreisspiel_timeblock ON bilanzkreisspiel_day.day_id=bilanzkreisspiel_timeblock.timeblock_day_id WHERE auth_user.username=%s', [mname])                 
            return render(request, 'bilanzkreisspiel/index.html', {'prof': gamer, 'days': Day.objects.all().filter(day_user=request.user), 'timebs': timebs})
            
        else:
            mname = request.user.username
            timebs = Timeblock.objects.raw('SELECT bilanzkreisspiel_timeblock.timeblock_id FROM (auth_user INNER JOIN bilanzkreisspiel_day ON auth_user.id = bilanzkreisspiel_day.day_user_id) INNER JOIN bilanzkreisspiel_timeblock ON bilanzkreisspiel_day.day_id=bilanzkreisspiel_timeblock.timeblock_day_id WHERE auth_user.username=%s', [mname])                 
            return render(request, 'bilanzkreisspiel/index.html', {'prof': gamer, 'days': Day.objects.all().filter(day_user=request.user), 'timebs': timebs})
         
    else:
        form_login = LoginForm()
        return render(request, 'gamemaster/login.html', {'form_login': form_login})
            

def init_game(request):
    init_days(request)
    init_timeblocks(request)
    request.user.profile.bks_status=1
    request.user.profile.bks_timeblock=Timeblock.objects.get(timeblock_day=Day.objects.get(day_user=request.user,day_number=0), timeblock_number=0);
    request.user.profile.save()

def init_days(request):
    number_of_days = NUMBER_DAYS
    
    for i in range(number_of_days):
        Day(day_user=request.user,day_number=i).save()
    
    
def init_timeblocks(request):
    number_of_timeblocks_aday = NUMBER_TIMEBLOCKS
    number_of_days = NUMBER_DAYS
    dur = DURATION_PER_DAY
    
    for k in range(number_of_days):
        for i in range(number_of_timeblocks_aday):
            Timeblock(timeblock_day=Day.objects.get(day_user=request.user,day_number=k),timeblock_number=i,timeblock_duration=dur).save()
        
        
def init_reset(request):
    number_of_timeblocks_aday = NUMBER_TIMEBLOCKS
    number_of_days = NUMBER_DAYS
    dur = DURATION_PER_DAY
    
    Timeblock.objects.filter(timeblock_day=Day.objects.filter(day_user=request.user)).delete()
    Day.objects.filter(day_user=request.user).delete()
    
    request.user.profile.bks_status=False
    request.user.profile.save()
    
                
def setNextTimeblock(request):
    gamer = request.user.profile
    if gamer.bks_timeblock.timeblock_number==NUMBER_TIMEBLOCKS-1:
        if gamer.bks_timeblock.timeblock_day.day_number<NUMBER_DAYS-1:
            gamer.bks_timeblock.timeblock_number=0
        setNextDay(request)
    else:
        gamer.bks_timeblock = Timeblock.objects.get(timeblock_day=gamer.bks_timeblock.timeblock_day, timeblock_number=(gamer.bks_timeblock.timeblock_number+1))    
            
    
def setNextDay(request):
    gamer = request.user.profile
    
    if gamer.bks_timeblock.timeblock_day.day_number+1==NUMBER_DAYS:
        print ('Du bist beim letzten Tag (dayfunction)')
    else:
        gamer.bks_timeblock = Timeblock.objects.get(timeblock_number=gamer.bks_timeblock.timeblock_number, timeblock_day=(Day.objects.get(day_user=request.user, day_number=(gamer.bks_timeblock.timeblock_day.day_number+1) )))
            
            
        
        
        