from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
# Create your models here.
class Fpo_Registeration(models.Model):
 fpo_username=models.CharField(max_length=50)
 fpo_name=models.CharField(max_length=50)
 fpo_area=models.CharField(max_length=500)
 fpo_email=models.CharField(max_length=500)
 
 area_pincode=models.IntegerField(null=True)
 total_members=models.IntegerField(null=True)
 fpo_img = models.ImageField(upload_to='images/FPO')
#  description=models.TextField()
 
 
 def __str__(self):
  return self.fpo_name
 

class Product(models.Model):
 CATEGORY_CHOICES = (
        ('Dairy', 'Dairy'),
        ('Grain', 'Grain'),
        ('Fruit', 'Fruits'),
    )
 product_by = models.ForeignKey(User, on_delete=models.CASCADE, default=True)
 product_name = models.CharField(max_length=50) 
 product_category = models.CharField(max_length=6, choices=CATEGORY_CHOICES)
 product_price =  models.IntegerField() 
 product_description = models.TextField()
 product_img1 = models.ImageField(upload_to='images/product', default='images/product/cart.png') 
 product_img2 = models.ImageField(upload_to='images/product', default='images/product/cart.png') 
 product_img3 = models.ImageField(upload_to='images/product', default='images/product/cart.png') 
 product_img4 = models.ImageField(upload_to='images/product', default='images/product/cart.png') 
 product_img5 = models.ImageField(upload_to='images/product', default='images/product/cart.png') 
 rating=models.IntegerField(null=True)
 def __str__(self):
  return self.product_name
 def get_absolute_url(self):
  return reverse('store')

class Cart(models.Model):
 cartuser=models.ForeignKey(User, on_delete=models.CASCADE, default=True)
 name = models.CharField(max_length=50) 
 price =  models.IntegerField() 
 
 img = models.ImageField(upload_to='images/') 

 def __str__(self):
  return self.name
  