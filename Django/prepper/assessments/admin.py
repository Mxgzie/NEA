from django.contrib import admin
from .models import Question, Answer, Markscheme
# Register your models here.

admin.site.register(Question) #Allows us to view, manage and CREATE question model instances through the online Django admin page
admin.site.register(Answer)
admin.site.register(Markscheme)