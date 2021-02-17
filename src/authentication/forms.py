from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'username'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'password'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean(self, *args, **kwargs):
        data = super(LoginForm, self).clean(*args, **kwargs)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('usuario o clave incorrecta')
        return data

    def save(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class SignupForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'password'}))
    confirmation = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'confirm password'}))

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean_username(self, *args, **kwargs):
        data = self.cleaned_data
        username = data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('username ya en uso')
        return username

    def clean_email(self, *args, **kwargs):
        data = self.cleaned_data
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email ya en uso')
        return email

    def clean(self, *args, **kwargs):
        data = super(LoginForm, self).clean(*args, **kwargs)
        password = data.get('password')
        confirmation = data.get('confirmation')
        if password and confirmation and password != confirmation:
            self.add_error('confirmation', 'passwords no coinciden')
        return data

    def save(self, *args, **kwargs):
        data = self.cleaned_data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        return user


class RegisterForm(AuthenticationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput)
    first_name = forms.CharField(required=True, widget=forms.TextInput)
    last_name = forms.CharField(required=True, widget=forms.TextInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2', )
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields.get(field).label = field.replace("_", ' ')
            self.fields.get(field).widget.attrs.update(
                {'class': 'form-control', 
                 'placeholder': self.fields.get(field).label}
            )
