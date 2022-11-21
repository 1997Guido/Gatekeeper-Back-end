from django.db import models
import string
import random

def generate_unique_id():
    length = 8
    
    while True:
        uid = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Users.objects.filter(uid=uid).count() == 0:
            break
        
    return uid


# Create your models here.
class Users(models.Model):
    first_name = models.CharField(max_length=32, default="")
    last_name = models.CharField(max_length=64, default="")
    age = models.IntegerField((""))
    date_created = models.DateField(auto_now_add=True)
    admin = models.BooleanField(default=False)
    