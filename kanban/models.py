from django.db import models
from django.contrib.auth.models import User

class Column(models.Model):
    title = models.CharField(max_length=100)

class Card(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name="cards")

class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    columns = models.ManyToManyField(Column)
