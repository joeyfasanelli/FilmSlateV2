from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Reaction(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home', kawrgs={'pk': self.id})

class MovieReview(models.Model):
    movie_review = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    reactions = models.ManyToManyField(Reaction)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.movie_review
        
    def get_absolute_url(self):
        return reverse('reviews_detail', kwargs={'movie_review_id': self.id})


class TvReview(models.Model):
    tv_review = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tv_id = models.IntegerField()
    reactions = models.ManyToManyField(Reaction)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tv_review
        
    def get_absolute_url(self):
        return reverse('reviews_detail', kwargs={'tv_review_id': self.id})


class Movie(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    reactions = models.ManyToManyField(Reaction)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'movie_id': self.id})