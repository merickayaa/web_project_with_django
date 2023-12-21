from django.contrib import admin
from .models import Messages,Thread
# Register your models here.
admin.site.register(Thread)

admin.site.register(Messages)