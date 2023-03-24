from django.contrib import admin
from hrv.models import UserProfile,Data
from django.contrib.auth.models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('user',)}
    #list_display = ('username', 'email', 'age')
admin.site.register(UserProfile,UserAdmin)
admin.site.register(Data)
