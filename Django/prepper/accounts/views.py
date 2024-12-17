from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def register(request): #Allows user to REGISTER an account for the FIRST time
    if request.user.is_authenticated:
        return redirect("/home")
    
    if request.method == "POST": #Checks if the user is submitting data to CREATE an account for the FIRST time
        form = RegisterForm(request.POST) #Create an instance of RegisterForm with the POST data (See accounts/forms.py for explanation of the class)
        if form.is_valid():
            user = form.save() #If the data in the form meets the validation criteria defined in the form class, save it to the database
            login(request,user) #Built in Django function that creates a "logged in" session for the user. This means that the user's 
            #authentication status is stored in the session and they won't need to log in again until they log out OR the session expires
        return redirect("/home") 
    else: #If the user isn't submitting data, e.g when they're first loading the login page
        form = RegisterForm() #Create an empty instance of the form for the user to enter data in
    
    return render(request, "register/register.html", {"form": form}) #Render the login template with the form instance created based on if its a GET or POST request

def user_login(request):
    if request.user.is_authenticated:
        return redirect("/home")
    
    if request.method == "POST":  # Checks if the user is submitting login data (e.g after they've typed the details and click login)
        form = AuthenticationForm(request, data=request.POST)  # Creates an instance of the Built-in Django authentication form w/ the POST data
        if form.is_valid():  # Validates the submitted data (e.g., correct username and password)
            username = form.cleaned_data.get("username") #Fetches the value from the created dictionary of valid inputs (form.cleaned_data) after running form.isvalid() that has the corresponding key "username"
            password = form.cleaned_data.get("password") #Fetches the value from the created dictionary of valid inputs (form.cleaned_data) after running form.isvalid() that has the corresponding key "password"
            user = authenticate(request, username=username, password=password)  # Searches the user DB to authenticate the user and store a "User" object that represents the authenticated user. If details are incorrect, user will store "None"
            if user is not None:  # Checks if the authentication was successful. If it wasn't, user would store None
                login(request, user)  # Logs the user in
                return redirect("/home")  # Redirect to home page after successful login
    else:  # If the user is not submitting data, show an empty login form
        form = AuthenticationForm()

    return render(request, "register/login.html", {"form": form})  # Render the login template with the form


def registerOrLogin(request):
    return render(request, "register/registerOrLogin.html")
