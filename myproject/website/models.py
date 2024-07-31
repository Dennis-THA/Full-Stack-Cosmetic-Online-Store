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
    
    # def save(self, *args, **kwargs):
    #     # Hash the password before saving
    #     self.password = make_password(self.password)
    #     super(Member, self).save(*args, **kwargs)
    
class Item(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_label = models.CharField(max_length=20, default='')
    image = models.ImageField(upload_to='item_images')
    image_hover = models.ImageField(upload_to='item_images')



    def __str__(self):
        return self.title
