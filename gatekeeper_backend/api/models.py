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
    class Meta:  
        verbose_name_plural = 'Users'
    GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
    )
    emailadress = models.CharField(max_length=32, null=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=False, null=False)
    first_name = models.CharField(max_length=32, null=False)
    last_name = models.CharField(max_length=64, null=False)
    age = models.IntegerField(null=False)
    date_created = models.DateField(auto_now_add=True, null=False)
    admin = models.BooleanField(default=False, null=False)
    def __str__(self):
        return self.last_name
    