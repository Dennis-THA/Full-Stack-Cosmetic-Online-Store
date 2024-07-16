from django.db import models
from django.contrib.auth.hashers import make_password

class Member(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=128) 
    age = models.PositiveIntegerField() 
    phone = models.CharField(max_length=15)  
    


    def __str__(self):
        return f"{self.fname} {self.lname}"
    
    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.password = make_password(self.password)
        super(Member, self).save(*args, **kwargs)
    
