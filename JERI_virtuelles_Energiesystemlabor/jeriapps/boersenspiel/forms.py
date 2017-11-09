from django import forms

class bidscoal(forms.Form):
    kw11=forms.FloatField(label='Nr.1')
    kw12=forms.FloatField(label='Nr.2')
    kw13=forms.FloatField(label='Nr.3')
    kw14=forms.FloatField(label='Nr.4')

class bidsgas(forms.Form):
    kw21=forms.FloatField(label='Nr.1')
    kw22=forms.FloatField(label='Nr.2')
    kw23=forms.FloatField(label='Nr.3')
    kw24=forms.FloatField(label='Nr.4')
    
class bidswater(forms.Form):
    kw31=forms.FloatField(label='Nr.1')
    kw32=forms.FloatField(label='Nr.2')
    kw33=forms.FloatField(label='Nr.3')
    kw34=forms.FloatField(label='Nr.4')
    
class einstellungenForm(forms.Form):
    Runde=forms.IntegerField(label='Spielrunde')
    Spiel=forms.IntegerField(label='ID des Spiels')
    AT_CHOICES=((1,'Pay-as-bid'),(2,'Uniform'))
    auctiontype=forms.ChoiceField(choices=AT_CHOICES, label='Auktionstype')
    nextround=forms.DateTimeField(label='Start der naechsten Runde')
    rundenzeit=forms.IntegerField(label='Laenge der Runden in Sekunden')
