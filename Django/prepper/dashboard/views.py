from django.shortcuts import render, redirect

# Create your views here.
def home(request): #Allows user to REGISTER an account for the FIRST time
    if request.user.is_authenticated:
        return render(request, "dashboard.html") #Render the login template with the form instance created based on if its a GET or POST request
    else:
        return redirect("/")
