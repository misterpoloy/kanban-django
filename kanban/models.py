from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Column(models.Model):
    title = models.CharField(max_length=100)
    cards = models.ManyToManyField(Card)

class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    columns = models.ManyToManyField(Column)
