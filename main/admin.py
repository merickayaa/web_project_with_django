from django.contrib import admin
from .models import User, Post,LikePost,Follower,Comment
# Register your models here.

admin.site.register(User)
class UserAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('username',)}

admin.site.register(Post)

admin.site.register(LikePost)

admin.site.register(Follower)

admin.site.register(Comment)
