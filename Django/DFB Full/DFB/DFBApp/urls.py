#Created by us since it isn't auto generated when you first create the app
#File that allows us to connect the views (functions to run) based on the different URLs that a user types
# E.g: url/path-1 -> view1 

from django.urls import path
from . import views #Import views from the current directory


urlpatterns = [
    # path("", views.index, name= "index"), #This will not display anything (Refer to base.html for explanation)
    #Recieves paths from the main urls.py file. If (root)/ was typed, then "" is sent to this file, and so the index view function from the views 
    # module is activated
    # name="index" is an optional name for the URL pattern. Giving a name to the URL pattern allows you to refer to it in other places in your code
    # (like templates or redirects), instead of hardcoding the URL path. Good because if the URL path ever changes, you only need to update it here
    # and not everywhere in your project.

    path("<int:id>",views.listViewById), 
    #If the url is xxxxx.com/5 the variable "id" will store "5" as an integer. This value then gets passed to the idbs1 function
    #Since the idbs1 function has the parameters "request" and "id", the path method will be able to pass this "id" variable from the URL
    #To the idbs1 function's "id" parameter. However, if the function's parameter name changes e.g "idNum", then the integer 5 will not be able 
    #to be passed to the idbs1 function's "idNum" parameter because the variable name here "id" doesn't match the functions arguement

    path("<str:name>",views.listViewByName),
    #If the url is xxxxx.com/bob the variable "name" will store "bob" as an string. This value then gets passed to the idbs2 function
    #Since the idbs2 function has the parameters "request" and "name", the path method will be able to pass this "name" variable from the URL
    #To the idbs1 function's "name" parameter. However, if the function's parameter name changes e.g "username", then the name string can't
    #be passed to the idbs2 function's "username" parameter because the variable name here "name" doesn't match the functions arguement

    path("home/",views.home),

    path("create/", views.create, name="create")
]
#Django looks at this list to determine which view should handle a specific URL.
