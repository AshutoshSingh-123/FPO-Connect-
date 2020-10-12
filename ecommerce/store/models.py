from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField
# Create your models here.
class Fpo_Registeration(models.Model):
 
 fpo_category = models.CharField(max_length=100, null=True, blank=True)
 fpo_username=models.CharField(max_length=50)
 fpo_name=models.CharField(max_length=50)
 fpo_area=models.CharField(max_length=500)
 fpo_email=models.CharField(max_length=500)
 fpo_mobile1=models.IntegerField(null=True)
 fpo_mobile2=models.IntegerField(null=True)
 fpo_description=models.TextField()

 area_pincode=models.IntegerField(null=True)
 total_members=models.IntegerField(null=True)
 fpo_img = models.ImageField(upload_to='images/FPO')

 
 
 def __str__(self):
  return self.fpo_name
 
 

class Product(models.Model):
 CATEGORY_CHOICES = (
        ('Dairy', 'Dairy'),
        ('Grain', 'Grain'),
        ('Fruit', 'Fruits'),
    )
 UNIT = (
        ('Kg', 'Kg'),
        ('Liter', 'Liter'),
        ('Meter', 'Meter'),
    )
 product_by = models.ForeignKey(User, on_delete=models.CASCADE, default=True)
 product_name = models.CharField(max_length=50) 
 product_category = models.CharField(max_length=6, choices=CATEGORY_CHOICES, null=True, blank=True)
 product_unit = models.CharField(max_length=6, choices=UNIT)
 product_price =  models.FloatField(null=True) 
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
 cartuser_email=models.CharField(max_length=50, null=True)
 date_added_on=models.DateTimeField(default=timezone.now)
 by_fpo=models.ForeignKey(Fpo_Registeration, on_delete=models.CASCADE, default=True)
 fpo_id=models.IntegerField(null=True) 
 name = models.CharField(max_length=50) 
 price =  models.IntegerField() 
 
 img = models.ImageField(upload_to='images/') 

 def __str__(self):
  return self.name



class Ngo_Registeration(models.Model):
 ngo_username=models.CharField(max_length=50)
 ngo_name=models.CharField(max_length=50)
 ngo_area=models.CharField(max_length=500)
 ngo_email=models.CharField(max_length=500)
 ngo_mobile1=models.IntegerField(null=True)
 ngo_mobile2=models.IntegerField(null=True)
 ngo_description=models.TextField()

 area_pincode=models.IntegerField(null=True)
 
 ngo_img = models.ImageField(upload_to='images/NGO')

class Service(models.Model):
  UNIT = (
        ('Hrs.', 'Hrs.'),
        ('Netting', 'Netting'),
        ('Day', 'Day'),
    )
  service_unit = models.CharField(max_length=20, choices=UNIT)
  service_price =  models.FloatField() 
  service_by1=models.ForeignKey(User, on_delete=models.CASCADE, default=True)
  service_by=models.ForeignKey(Ngo_Registeration, on_delete=models.CASCADE, default=True)
  date_posted=models.DateTimeField(default=timezone.now)
  service_description=RichTextField(blank=True, null=True)
  service_title=models.CharField(max_length=50)
  def get_absolute_url(self):
   return reverse('services')