from django.contrib import admin
from .models import UserProfile, UserSkill, PostImage
# Register your models here.


admin.site.register(UserProfile)
admin.site.register(UserSkill)
admin.site.register(PostImage)
