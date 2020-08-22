from django.db import models
import bcrypt
import re

#Email Regex101
EMAIL_MATCH = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    #Validating the User Registration Information
    def validations(self, form_data):
        errors = {}
        if len(form_data['first_name']) < 1:
            errors['first_name'] = 'Must enter a first name' 

        if len(form_data['last_name']) < 1:
            errors['last_name'] = 'Must enter a last name' 
        
        if len(form_data['email']) < 1:
            errors['email'] = 'Must enter an email'
        
        if len(form_data['password']) < 1:
            errors['password'] = 'Must enter an password'
        
        if len(form_data['confirm']) < 1:
            errors['confirm'] = 'Must confirm your password'
        
        if form_data['password'] != form_data['confirm']:
            errors['confirm'] = 'Passwords do not match'   
        
        if not EMAIL_MATCH.match(form_data['email']):
            errors['email'] = 'Invalid Email'
        
        users_with_email = self.filter(email=form_data['email'])
        if users_with_email:
            errors['email'] = 'Email Is Already Registered'                 
        return errors
    #Registering A User
    def register(self, form_data):
        hash1 = bcrypt.hashpw(form_data['password'].encode(),bcrypt.gensalt()).decode()
        self.create(
            first_name = form_data['first_name'],
            last_name = form_data['last_name'],
            email = form_data['email'],
            password = hash1
        )
    #Authenticating Login Information
    def authenticate(self, email, password):
        users_with_emails = self.filter(email = email)
        if not users_with_emails:
            return False
        user = users_with_emails[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())





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
    chef = models.ForeignKey(User, related_name = 'recipes_posted', on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name = 'recipes_liked')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    content = models.TextField()
    commentor = models.ForeignKey(User, related_name = 'comments_made', on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='comments_liked')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
