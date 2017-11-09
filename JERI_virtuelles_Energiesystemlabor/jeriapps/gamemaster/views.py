# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.template.context_processors import request
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from gamemaster.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import *

# Create your views here.

def register(request):
    if request.method == 'POST':
        form_reg = RegForm(request.POST)
        form_login = LoginForm(request.POST)
        if form_reg.is_valid():
            
            username = form_reg.cleaned_data.get('username')
            password = form_reg.cleaned_data.get('password')
            password_req = form_reg.cleaned_data.get('password_req')
            
            if password == password_req:
                user = User.objects.create_user(username,'',password)
                user.save()
                
                g = Group.objects.get(name='Student') 
                g.user_set.add(user)
                form_login = LoginForm()
                return login_view(request)
            else:
                wrong = 'Passwörter stimmen nicht überein'
                return render(request, 'gamemaster/index.html', {'form_reg': form_reg, 'wrong': wrong}) 
            
    else:
        form_reg = RegForm()
        return render(request, 'gamemaster/index.html', {'form_reg': form_reg})
    
def start_lobby(request):
    wrongteacherpassword = ''
    if request.POST.get('submit'):
        
        tName = request.POST.get('TeacherName')
        tPassword = request.POST.get('TeacherPassword')
        user = authenticate(username = tName,password = tPassword)
        
        if user is not None:
            login(request, user)
            
            lobby = Lobby()
            lobby.lobby_name = request.POST.get('name')
            lobby.lobby_password =request.POST.get('PasswordLobby')
            lobby.lobby_modus = request.POST.get('gamemode')
            lobby.save()
            
        else:
            wrongteacherpassword = 'wrong teacher-password/name!'
            return render(request, 'gamemaster/teacher_login.html',{'wrong': wrongteacherpassword,})
        
    return render(request, 'gamemaster/teacher_login.html') #bearbeiten wenn Lobbyviews fertig sind!!!

def lobby(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            data = Lobby.objects.get(lobby_name=request.POST.get("lobbyname"))
            Profile.objects.filter(user=request.user).update(lobby=data)
            lobby_user = Profile.objects.filter(lobby=data)
            return render(request, 'gamemaster/lobby.html', {'data': data, 'lobby_user': lobby_user})
        else:
            data=Profile.objects.get(user=request.user).lobby
            lobby_user = Profile.objects.filter(lobby=data)
            return render(request, 'gamemaster/lobby.html', {'data': data, 'lobby_user': lobby_user})
    else:
        form_login = LoginForm(request.POST)
        if form_login.is_valid():
            
            username = form_login.cleaned_data.get('username')
            password = form_login.cleaned_data.get('password')
            
            user = authenticate(request,username=username,password=password)
            
            if user is not None:
                login(request, user)
                data=Lobby.objects.all()
                return render(request, 'gamemaster/all_lobbys.html', {'data': data})    
            else:
                wrong = 'Nickname oder Passwort falsch!'
                return render(request, 'gamemaster/login.html', {'form_login': form_login, 'wrong': wrong}) 
            
        
 
def all_lobbys(request):
    if request.user.is_authenticated():
        data=Lobby.objects.all()
        return render(request, 'gamemaster/all_lobbys.html', {'data': data})
    else:
        form_login = LoginForm(request.POST)
        if form_login.is_valid():
            
            username = form_login.cleaned_data.get('username')
            password = form_login.cleaned_data.get('password')
            
            user = authenticate(request,username=username,password=password)
            
            if user is not None:
                login(request, user)
                data=Lobby.objects.all()
                us = Profile.objects.all()
                return render(request, 'gamemaster/all_lobbys.html', {'data': data, 'us': us })    
            else:
                wrong = 'Nickname oder Passwort falsch!'
                return render(request, 'gamemaster/login.html', {'form_login': form_login, 'wrong': wrong}) 
            
        
        
    
def login_view(request):        
    form_login = LoginForm()
    return render(request, 'gamemaster/login.html', {'form_login': form_login})
        
def logout_view(request):
    form_login = LoginForm(request.POST)
    Profile.objects.filter(user=request.user).update(lobby='0')
    logout(request)
    wrong = 'Sie wurden erfolgreich ausgeloggt'
    return render(request, 'gamemaster/login.html', {'form_login': form_login, 'wrong': wrong}) 