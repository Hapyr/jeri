from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    url(r'^$', views.login, name='start'),
    url(r'^login', views.login, name='login'),
    url(r'^signup',views.signup, name='signup'),
    url(r'^handler', views.handler, name='handler'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^admin', views.admin, name='admin'),
    url(r'^prefs', views.prefs, name='prefs'),
    url(r'^markets', views.externalmarkets, name='markets'),
    url(r'^hs', views.highscores, name='hs'),
    url(r'^rs', views.auctionsresults,name='results')
    
    ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
