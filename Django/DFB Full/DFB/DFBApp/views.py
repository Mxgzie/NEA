from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from urllib.parse import unquote
from .forms import CreateNewList
# HttpReponse allows you to send HTTP responses directly to the user, typically used to send raw HTML, text, or other data.

# Create your views here.

#Handles incoming web requests and returns a response to the user
def index(request): # "response" parameter represents the incoming HTTP request.
    #return HttpResponse("<h1>Migz' Site</h1>") - This is inefficient as we could use HTML template files instead of hardcoding HTML within brackets
    #Returns an HTTP response containing the HTML <h1>Migz' Site</h1> back to
    #the user's browser - The object contains information about the user's
    #request, like what URL they visited, their browser info, etc.
    
    return render(request, "DFBApp/base.html", {}) #The render function can take a dictionary of variables that can be used to dynamically change webpages based on different variable values

def v1(request):
    return HttpResponse("<h1>View 1</h1>")

def idbs1(request, id): #Retrieves a ToDoList by its id
    ls = ToDoList.objects.get(id=id) 
    #Objects is the default manager for the ToDoList TABLE which allows you to interact with the database
    #.get() is a method that retrieves a single record from the table where the value "id" matches the value passed to the function
    return render(request, "DFBApp/base.html", {})
    #Displays the name of the ToDoList (%s is a placeholder for substitution, and the value in %ls.name will be placed here)


def listView(request, name): #Retrieves a ToDoList by its name
    name = unquote(name) #Converts "First%20List" to "First List"
    ls = ToDoList.objects.get(name=name)
    #Objects is the default manager for the ToDoList TABLE which allows you to interact with the database
    #.get() is a method that retrieves a single record from the table where the string "name" matches the string passed to the function
    #The record is then stored in the variable "ls"

    items = ls.item_set.all()
    #items_set allows us to get items related to the ToDoList we stored in ls
    #.get() allows us to specify the item by a certain value (e.g its id)
    #.all() allows us to get all the items under the stored ToDoList in ls
    #return HttpResponse("<h1>%s</h1><br></br><p>%s</p>" %(ls.name, str(items.text)))

    return render(request, "DFBApp/list.html",{"ls":ls})

def home(request):
    return render(request, "DFBApp/home.html", {}) #Renders the home.html file

def create(request):
    if request.method == "POST":
        form = CreateNewList(request.POST)
         
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
        
        return HttpResponseRedirect("%i" %t.id)
    else:
        form = CreateNewList
    return render(request, "DFBApp/create.html", {"form":form})

#pass: 12345 / #user: migzm

