from django.contrib import admin
from boersenspiel.models import Spieler,kraftwerke, spielerkraftwerke, gebote, brennstoff, brennstoffpreise, lastgang, ergebnisse, boersenpreise, co2preise, einstellungen


# Register your models here.
admin.site.register(Spieler,)
admin.site.register(kraftwerke,)
admin.site.register(spielerkraftwerke,)
admin.site.register(gebote,)
admin.site.register(brennstoff,)
admin.site.register(brennstoffpreise,)
admin.site.register(lastgang,)
admin.site.register(ergebnisse,)
admin.site.register(boersenpreise,)
admin.site.register(co2preise,)
admin.site.register(einstellungen,)
