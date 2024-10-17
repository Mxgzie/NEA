from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.
def register(request):
    if request.method == "POST": #If the user is submitting data
        form = RegisterForm(request.POST) #Create an instance of RegisterForm with the POST data (See forms.py for explanation of the class)
        if form.is_valid():
            form.save() #If the data in the form meets the criteria defined in the form class, save it to the database
        return redirect("/home")
    else: #If the user isn't submitting data, e.g when they're first loading the login page
        form = RegisterForm() #Create an empty instance of the form for the user to enter data in
    
    print("Form context ASDASDSA:", form)
    return render(request, "register/register.html", {"form": form}) #Render the login template with the form instance created based on if its a GET or POST request
