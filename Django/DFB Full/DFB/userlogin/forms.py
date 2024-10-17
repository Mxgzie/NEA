from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm): #Defines a new register form that inherits properties + methods from DJANGO'S USER CREATION FORM
    email = forms.EmailField() #Creates an email field instance, provided by DJANGO, that automatically validates the input

    class Meta: #Tells Django how the form should behave and which database it should connect to
        model = User #Tells django that this model is connected to the user database, so any data entered in the form should be saved to the user table
        #This line also allows for automatic field generation and validation rules
        fields = ["username","email","password1","password2"] #Defines the fields from DJANGO'S USER MODEL that will be displayed IN ORDER in the form
            #username, password1, and password2 are pre-built default fields in the django userform, email is our own custom one