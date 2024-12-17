from django.db import models
from django.contrib.auth.models import User  # Import the User model

# Create your models here.

class Question(models.Model):
    text = models.TextField()  # The actual question prompt
    topic = models.CharField(max_length=100)  # The topic of the question (e.g., "Data Structures")
    exam_board = models.CharField(max_length=7)  # For example, "AQA" or "Edexcel"
    Qnum = models.CharField(max_length=5)
    exam_year = models.IntegerField()  # The year the question was from (if applicable)
    marks = models.IntegerField()  # Total marks for the question
    exam_paper = models.IntegerField()
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)  # Optional image field


    def __str__(self):
        return f"{self.topic} - {self.text[:50]}..."  # Show the topic and a snippet of the question text


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    question = models.ForeignKey('Question', on_delete=models.CASCADE)  # Link to the question
    answer_text = models.TextField()  # Field to store the user's answer
    submitted_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f"Answer by {self.user.username} for {self.question.id}"
    

class Markscheme(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)  # Link to the question
    points = models.TextField()
    question_marks = models.IntegerField()

