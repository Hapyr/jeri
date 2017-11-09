from django import forms

class RegForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password_req = forms.CharField(label='password wiederholen', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Nickname'
        self.fields['password'].widget.attrs['placeholder'] = 'Passwort'
        self.fields['password_req'].widget.attrs['placeholder'] = 'Passwort wiederholen'
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password_req'].widget.attrs['class'] = 'form-control'
        
        self.fields['username'].widget.attrs['name'] = 'reg_username'
        self.fields['password'].widget.attrs['name'] = 'reg_password'
        self.fields['password_req'].widget.attrs['name'] = 'reg_password_req'
        
class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Nickname'
        self.fields['password'].widget.attrs['placeholder'] = 'Passwort'
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        
        
        self.fields['username'].widget.attrs['name'] = 'login_username'
        self.fields['password'].widget.attrs['name'] = 'login_password'
        
                