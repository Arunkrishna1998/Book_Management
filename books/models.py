from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    authors = models.CharField(max_length=255)
    genre = models.CharField(max_length=50)
    publication_date = models.DateField()
    description = models.TextField(blank=True, null=True)


class ReadingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class BookReadingList(models.Model):
    reading_list = models.ForeignKey(ReadingList, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.IntegerField()
