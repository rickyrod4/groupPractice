from django.db import models
import bcrypt
import re

#Email Regex101
EMAIL_MATCH = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    #recipes_posted (Post)
    #recipes_liked (Post)
    #comments_made (Comment)
    #comments_liked(Comment)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Post(models.Model):
    title = models.CharField(max_length=255)
    recipe = models.TextField()
    chef = models.ForiegnKey(User, related_name = 'recipes_posted', on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name = 'recipes_liked')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    content = models.TextField()
    commentor = models.ForiegnKey(User, related_name = 'comments_made', on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='comments_liked')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
