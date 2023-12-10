from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
import uuid
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.template.defaultfilters import slugify



# Create your models here.
class User(AbstractUser):
    student_no = models.CharField(max_length=12, unique=True, help_text="4,5 ve 6. rakamlar 214 veya 114 olmalıdır", null=True)   
    profileimg = models.ImageField(upload_to='profile_images', default='user.png')
    job = models.CharField(max_length=30, blank=True, null=True)
    company_name = models.CharField(max_length=30, blank=True, null=True)
    TYPE_OF_WORK_OPTIONS = [
        ('uzaktan', 'Uzaktan'),
        ('ofisten', 'Ofisten'),
        ('hibrit', 'Hibrit'),
    ]

    type_of_work = models.CharField(
        max_length=20,
        choices=TYPE_OF_WORK_OPTIONS,
        blank=True,
        null=True,
    )

    COLLEGE_OPTIONS = [
        ('edremit', 'Edremit Meslek YüksekOkulu'),
        ('altinoluk', 'Altınoluk Meslek YüksekOkulu'),
        ('balikesir', 'Balıkesir Meslek YüksekOkulu'),
    ]

    college = models.CharField(
        max_length=50,
        choices=COLLEGE_OPTIONS,
        blank=True,
        null=True,
    )
    
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    birthday = models.DateField(max_length=10, null=True, blank=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("dashboard", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)



class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    # user_id = models.IntegerField()
    image=models.ImageField(upload_to='post_images', null=True)
    caption= models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username
    

class LikePost(models.Model):
    post_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

