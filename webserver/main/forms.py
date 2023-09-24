from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User, Group

from .models import *
from .config import config

class createUserForm(UserCreationForm):
        class Meta:
            model = User
            fields = ['username', 'email', 'password1', 'password2']

class createServerAllocation(forms.Form):

    def getChoices(self, maxValue):
         Choices = [
              ( str(i) , i) for i in range(1, maxValue + 1)
         ]
         return Choices

    def isUserinGroutp(user, group):
         return user.groups.filter(name=group).exists()
         

    def __init__(self, user, *args, **kwargs):
        
        # set max Value of duration based on User
        maxValue = 0
        if user.is_superuser or user.groups.filter(name="admin").exists():
            maxValue = config['adminMaxAllocation']
        elif user.groups.filter(name="normalUser").exists():
             maxValue = config['normalMaxAllocation']

        
        super(createServerAllocation, self).__init__(*args, **kwargs)
        choices = self.getChoices(maxValue)
        self.fields['durationInHours'] = forms.ChoiceField(choices=choices)
    

class changeServerAllocation(forms.Form):
     id = forms.IntegerField(min_value=0)
     active = forms.BooleanField(required=False)

      