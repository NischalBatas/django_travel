from multiprocessing import managers
from tkinter import CASCADE
import webbrowser
from django.db import models

# Create your models here.
class Venue(models.Model):
    name=models.CharField("Venue Name",max_length=100,null=True,blank=True)
    address=models.CharField(max_length=100,null=True,blank=True)
    zip_code=models.CharField('Zip code',max_length=100,null=True,blank=True)
    phone=models.CharField('Phone',max_length=100,null=True,blank=True)
    web=models.URLField('Website Address')
    email_address=models.EmailField('Email Address')

    def __str__(self):
        return self.name

class MyClubUser(models.Model):
    first_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    email=models.EmailField('User Email Address')

    def __str__(self):
        return self.first_name+''+self.last_name

class Event(models.Model):
    name=models.CharField('Event Name',max_length=100,null=True,blank=True)
    event_date=models.DateTimeField()
    venue=models.ForeignKey(Venue,on_delete=models.CASCADE,blank=True,null=True)
    description=models.TextField(max_length=100,null=True,blank=True)
    attendees=models.ManyToManyField(MyClubUser,blank=True)

    def __str__(self):
        return self.name