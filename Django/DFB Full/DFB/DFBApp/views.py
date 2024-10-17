from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from urllib.parse import unquote
from .forms import CreateNewList
# HttpReponse allows you to send HTTP responses directly to the user, typically used to send raw HTML, text, or other data.

# Create your views here.

#Handles incoming web requests and returns a response to the user
# def index(request): # "response" parameter represents the incoming HTTP request.
#     #return HttpResponse("<h1>Migz' Site</h1>") - This is inefficient as we could use HTML template files instead of hardcoding HTML within brackets
#     #Returns an HTTP response containing the HTML <h1>Migz' Site</h1> back to
#     #the user's browser - The object contains information about the user's
#     #request, like what URL they visited, their browser info, etc.
#     ls = ToDoList.objects.all()
#     if request.method == "POST":
#         print("request.POST")
#         if request.POST.get("save"):
#             for item in ls:
#     return render(request, "DFBApp/base.html", {}) #The render function can take a dictionary of variables that can be used to dynamically change webpages based on different variable values

def listViewById(request, id): #Retrieves a ToDoList by its id
    ls = ToDoList.objects.get(id=id) 
    #Objects is the default manager for the ToDoList TABLE which allows you to interact with the database
    #.get() is a method that retrieves a single record from the table where the value "id" matches the value passed to the function
    
    if request.POST.get("save"): #Checks the data sent via POST from the client's browser and tries to retrieve the value associated with the key "save"
            #If the key exists in the data it means save was clicked and the statement evaluates to True
            for item in ls.item_set.all(): #Loops through all the items in the ToDoList instance retreived from the DB via item_set.all() command
                if request.POST.get("c"+str(item.id)) == "clicked": #Checks if the checkbox for the item was clicked 
                    item.complete = True 
                else:
                    item.complete = False

                item.save() #Saves the updated item.complete attribute back to the DB 
        
    elif request.POST.get("newItem"): #Checks the data sent via POST from the client's browser and tries to retrieve the value associated with the key "newItem"
        #If the key exists in the data it means addItem was clicked and the statement evaluates to True
        text = request.POST.get("new") #Retrieves the value from the input field labelled "new"

        if len(text) > 2:
            ls.item_set.create(text=text, complete=False)
            #A new item instance is created with text being set to the value from the input field, and complete being set to False
        else: #If the new item isn't 2 chars long, item is invalid
            print("invalid")
            
    return render(request, "DFBApp/list.html",{"ls":ls}) 
    #See listViewByName for explanation of code


def listViewByName(request, name): #Retrieves a ToDoList by its name
    name = unquote(name) #Converts "First%20List" to "First List"
    ls = ToDoList.objects.get(name=name)
    #Objects is the default manager for the ToDoList TABLE which allows you to interact with the database
    #.get() is a method that retrieves a single record from the table where the string "name" matches the string passed to the function
    #In this case, an instance of ToDoList is retrieved and stored in the variable "ls"

    items = ls.item_set.all()
    #items_set allows us to get items related to the ToDoList we stored in ls
    #.get() allows us to specify the item by a certain value (e.g its id)
    #.all() allows us to get all the items under the stored ToDoList in ls
    return render(request, "DFBApp/list.html",{"ls":ls}) 
    #Renders the list.html template which basically displays the list, and the items part of it, which is stored in ls
     #If the key was "list1", then the list has to be referred as list1 in the HTML

def home(request):
    return render(request, "DFBApp/home.html", {}) #Renders the home.html file

def create(request): # Creates a new toDoList
    if request.method == "POST": #Checks if the HTTP request is trying to send data to the server (e.g. user submitted a form)
        form = CreateNewList(request.POST) #Creates a new instance of the form with the data submitted by the user via the POST request (See forms.py)
        if form.is_valid(): #Checks if the form satisfies all the validation rules that it has (see forms.py)
            #When .is_valid() is called, a temporary dictionary called "cleaned_data" is created for each form submission with each key pair value
            # cleaned_data = {"name":"x","check":True}

            n = form.cleaned_data["name"] #Assigns the name value from the dictionary to n
            request.user.todolist_set.create(name=n)
            # t = ToDoList(name=n) #Creates a new instance of the ToDoList model (seel models.py) with the name set to the value in 'n'

        return HttpResponseRedirect("%i" %t.id) #Creates a new HTTP request to redirect the user to xxx/t.id/ where t.id would be an integer
        #This will therefore run the idbs1() view
    

    else: #If the HTTP request is not POST, e.g. if the user is trying to access the form for the first time, not submitting it
        form = CreateNewList #Creates a blank form instance with no data, usually used to display the empty form for the first before users add to it

    return render(request, "DFBApp/create.html", {"form":form}) 
    #Renders the create.html template with the "form" variable defined in this function passed into the template
    #If the key was "form1", then the form has to be referred as form1 in the HTML

#pass: 12345 / #user: migzm

