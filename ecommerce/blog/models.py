

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
# Create your models here.
class Post(models.Model):
  
 title=models.CharField(max_length=100)

 UNIT = (
        ('Technology', 'Technology'),
        ('Reserach', 'Reserach'),
        ('Story', 'Story'),
        ('Update', 'Update'),
        ('Policy', 'Policy'),
        ('Scheme', 'Scheme'),
    )
  
 category = models.CharField(max_length=200, choices=UNIT)
 tag = models.CharField(max_length=200, null=True, blank=True)
 content=RichTextField(blank=True, null=True)
 date_posted=models.DateTimeField(default=timezone.now)
 author=models.ForeignKey(User, on_delete=models.CASCADE)
#  image= models.ImageField(upload_to='knowledge_image', null=True)

 def __str__(self):
  return self.title

 def get_absolute_url(self):
  return reverse('post-detail', kwargs={'pk': self.pk})


class Document(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image= models.ImageField(upload_to='knowledge_image', null=True, blank=True)
    description = models.TextField( blank=True)
    
    document = models.FileField(upload_to='documents/', blank=True)
    link=models.URLField(max_length=200,  null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

