from django.db import models
from django.utils import timezone
from store.models import Fpo_Registeration
from django.contrib.auth.models import User
# Create your models here.
class Message(models.Model):

 from1=models.CharField(max_length=50)
 to=models.ForeignKey(Fpo_Registeration, on_delete=models.CASCADE, default=True)
 email=models.CharField(max_length=50)
 subject=models.CharField(max_length=500)
 message=models.TextField()
 phone=models.IntegerField()
 date=models.DateTimeField(default=timezone.now)

class Profile(models.Model):
 user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True,null=True)
 image=models.ImageField(default='default.jpg', upload_to='profile_pics')

 def __str__(self):
  return f'{self.user.username} Profile'