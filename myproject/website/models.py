from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone


class Member(models.Model):
    # user = models.OneToOneField(User, default=1, on_delete=models.CASCADE)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=128) 
    age = models.PositiveIntegerField() 
    phone = models.CharField(max_length=15)  
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True) 
    
    def save(self, *args, **kwargs):
        # Ensure that the password is hashed before saving
        if not self.pk or not Member.objects.get(pk=self.pk).password == self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fname} {self.lname}"
    
    
class Item(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_label = models.CharField(max_length=20, default='')
    image = models.ImageField(upload_to='item_images')
    image_hover = models.ImageField(upload_to='item_images')

    def __str__(self):
        return self.title

class VariationImage(models.Model):
    item = models.ForeignKey(Item, related_name='variation_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='variation_images/')

    def __str__(self):
        return f"Variation Image for {self.item.title}"
    


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40, blank=True)  # For anonymous users
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart for {self.user or 'Anonymous'} - Item: {self.item.title}"

    


class Review(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    profile_pic = models.ImageField(upload_to='profile_pics/', default='images/default_profile.webp')
    rating = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.title}"

