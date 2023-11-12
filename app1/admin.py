
# Register your models here.
from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'income', 'current_savings', 'goal']

admin.site.register(UserProfile, UserProfileAdmin)
