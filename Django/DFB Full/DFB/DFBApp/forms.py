from django import forms

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length = 200) #Label is the placeholder text that initally appears in a field
    check = forms.BooleanField(required=False) #Default required value is set to True