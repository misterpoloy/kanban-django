from django.db import models

class Card(models.Model):
    content = models.TextField()

class Column(models.Model):
    title = models.CharField(max_length=100)
    cards = models.ManyToManyField(Card)

class Board(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    columns = models.ManyToManyField(Column)
