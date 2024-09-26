from django.contrib import admin
from .models import ToDoList, Item

# Register your models here.
admin.site.register(ToDoList) #Registers the model so you can add, view, edit, or delete entries for that model from the Django admin panel
admin.site.register(Item)