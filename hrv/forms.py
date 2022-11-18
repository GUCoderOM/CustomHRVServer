from django import forms
from hrv.models import User
from django.contrib.auth.models import User
from hrv.models import UserProfile, UserWatch

WATCH_CHOICES= [
('TicWatch Pro 3 GPS', 'TicWatch Pro 3 GPS'),
('TicWatch Pro 2 GPS', 'TicWatch Pro 2 GPS'),
]

class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=120,)
    email = forms.EmailField(max_length=120,)
    #age = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput())
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = User
        fields = ('username','email','password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

class UserWatchForm(forms.ModelForm):
    watch = forms.CharField(label='Select your watch', widget=forms.Select(choices=WATCH_CHOICES))
    class Meta:
        model = UserWatch
        fields = ('watch',)
