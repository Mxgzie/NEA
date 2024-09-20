from django.shortcuts import render
from django.http import HttpResponse 
from .models import ToDoList, Item
# HttpReponse allows you to send HTTP responses directly to the user, typically used to send raw HTML, text, or other data.

# Create your views here.

#Handles incoming web requests and returns a response to the user
def index(request): # "response" parameter represents the incoming HTTP request.
    return HttpResponse("<h1>Migz' Site</h1>")
    #Returns an HTTP response containing the HTML <h1>Migz' Site</h1> back to
    #the user's browser - The object contains information about the user's
    #request, like what URL they visited, their browser info, etc.

def v1(request):
    return HttpResponse("<h1>View 1</h1>")

def idbs1(request, id):
    ls = ToDoList.objects.get(id=id)
    return HttpResponse("<h1>%s</h1>" %ls.name)

def idbs2(request, name):
    ls = ToDoList.objects.get(name=name)
    return HttpResponse("<h1>%s</h1>" %ls.name)

