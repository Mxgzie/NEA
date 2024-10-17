from django.db import models # Gives us tools to define how data will be structured and stored in the database.
from django.contrib.auth.models import User
#Models are representations of tables in a database - Each class in this file represents a table, and each class attribute represents a column 
# in that table

# Create your models here.

class ToDoList(models.Model): #Inheritance here tells Django to treat this as a database table
    name = models.CharField(max_length=200) #Creates a column in the table called name
    user = models.ForeignKey(User,on_delete=models.CASCADE) #Tells Django that every todolist we create will be linked to a user

    def __str__(self):
        return self.name
    
class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete = models.CASCADE) #Creates a relationship between the item table and todolist table
#ForeignKey creates a many-to-one relationship: many "Items" must be associated with one "ToDoList"
#If the ToDoList an Item is linked to is deleted, all the items linked to that list will also be deleted (this is called a "cascade delete").
    text = models.CharField(max_length=300) #Creates a column in the table called text
    complete = models.BooleanField() #Creates a column in the table called complete

    def __str__(self):
        return self.text

