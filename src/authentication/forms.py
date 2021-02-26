from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': field
            })

    def clean(self, *args, **kwargs):
        data = super(LoginForm, self).clean(*args, **kwargs)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError('usuario o clave incorrecta')
        return data

    def save(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class SignupForm(forms.Form):
    username = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"autofocus": "true"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    confirmation = forms.CharField(required=True, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': field,
            })

    def clean_username(self, *args, **kwargs):
        data = self.cleaned_data
        username = data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise ValidationError('username ya en uso')
        return username

    def clean_email(self, *args, **kwargs):
        data = self.cleaned_data
        email = data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError('email ya en uso')
        return email

    def clean(self, *args, **kwargs):
        data = super(SignupForm, self).clean(*args, **kwargs)
        password = data.get('password')
        confirmation = data.get('confirmation')
        if password and confirmation and password != confirmation:
            raise ValidationError('passwords no coinciden')
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


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput())
    first_name = forms.CharField(required=True, widget=forms.TextInput())
    last_name = forms.CharField(required=True, widget=forms.TextInput())

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


class ChangeProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        exclude = ('password',)
    
    def __init__(self, *args, **kwargs):
        super(ChangeProfileForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields.get(field).label = field.replace('_', ' ')
            self.fields.get(field).widget.attrs.update(
                {'class': 'form-control',
                'placeholder': self.fields.get(field).label}
            )
        del self.fields['password']
