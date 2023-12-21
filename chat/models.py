from django.db import models
from main.models import User
from datetime import datetime
# Create your models here.

class Thread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

class Messages(models.Model):
    theread = models.ForeignKey('Thread', related_name='+',on_delete=models.CASCADE,blank=True,null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+')
    body = models.CharField(max_length=100)
    image = models.ImageField(upload_to='messages_photos', blank=True,null=True)
    date = models.DateTimeField(default=datetime.now)
    is_read = models.BooleanField(default=False)


