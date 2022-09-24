from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField, IntegerField
from datetime import datetime,timedelta

# Create your models here.
class Usermember(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    user_address=models.CharField(max_length=255)
    user_mobile=models.CharField(max_length=255)
    user_gender=models.CharField(max_length=255)
    user_designation=models.CharField(max_length=255)
    user_photo=models.ImageField(upload_to='image/user')

    def __str__(self):
        return self.user

class Category(models.Model):
    category_name=models.CharField(max_length=255)
    language=models.CharField(max_length=255)

    

class book(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    book_name=models.CharField(max_length=255)
    book_image=models.ImageField(upload_to="image/",null=True)
    description=models.CharField(max_length=255)
    author=models.CharField(max_length=100)
    publication=models.CharField(max_length=100)
    price=models.IntegerField()
    quantity=models.IntegerField()

class requestbook(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    book=models.ForeignKey(book,on_delete=models.CASCADE,null=True)
    issuedays=models.IntegerField(default=30)


def get_expiry():
    return datetime.today() + timedelta(days=30)
class issuebook(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    book=models.ForeignKey(book,on_delete=models.CASCADE,null=True)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=get_expiry)


