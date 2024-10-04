from django import forms

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length = 200) #Label is the placeholder text that initally appears in a field
    check = forms.BooleanField(required=False) #Default required value is set to True

    #Validation rules:
    #1. name has a value entered, it has less than or only 200 characters, and the value can be casted/converted to the string
    #2. check has a boolean value assigned to it IF the checkbox were to be clicked