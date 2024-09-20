#Created by us since it isn't auto generated when you first create the app
#File that allows us to connect the views (functions to run) based on the different URLs that a user types
# E.g: url/path-1 -> view1 

from django.urls import path
from . import views #Import views from the current directory


urlpatterns = [
    path("", views.index, name= "index"),
    #Recieves paths from the main urls.py file. If (root)/ was typed, then "" is sent to this file, and so the index view function from the views 
    # module is activated
    # name="index" is an optional name for the URL pattern. Giving a name to the URL pattern allows you to refer to it in other places in your code
    # (like templates or redirects), instead of hardcoding the URL path. Good because if the URL path ever changes, you only need to update it here
    # and not everywhere in your project.

    path("v1/", views.v1, name= "view1"),
    #Recieves paths from the main urls.py file. If (root)/v1/ was typed, then "v1/" is sent to this file, and so the index view function from the 
    # views module is activated

    path("<int:id>",views.idbs1),

    path("<str:name>",views.idbs2)
]
#Django looks at this list to determine which view should handle a specific URL.
