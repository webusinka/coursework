# accounts/admin.py
from django.contrib import admin
from .models import Profile, CustomUser  
from django.contrib.auth.admin import UserAdmin

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_username')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'