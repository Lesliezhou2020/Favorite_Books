from django.db import models
import re
import bcrypt


class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = " Last_name should be at least 2 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):              
            errors['email'] = "Invalid email address!"
        
        if len(postData['password']) < 8:
            errors["password"] = " Password should be at least 8 characters"
        
        if postData['password'] != postData['confirm_PW']:
            errors['confirm_PW'] =  "Password does not match"     
        
        print(errors)
        return errors

    def login_validator(self, postData):
        errors = {}
        user_list_to_login = User.objects.filter(email=postData['login_email'])
        if len(user_list_to_login) == 0:
            errors['login_email'] = "There was a problem email"
        else:
            if not bcrypt.checkpw(postData['login_password'].encode(), user_list_to_login[0].password.encode()):
                erroes['login_password'] = "There was a problem password"
        
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors["title"] = "Book title should be at least 1 characters"
        if len(postData['desc']) < 5:
            errors["desc"] = "Book description must be at least 5 characters"

        return errors


class Book(models.Model):
    title = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, related_name="book_upladed", on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
    
    



