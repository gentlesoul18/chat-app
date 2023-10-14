from django.contrib import admin
from api.models import User, ChatMessage, Profile
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone_number']


class ProfileAdmin(admin.ModelAdmin):
    list_editable = ['verified',]
    list_display = ['user', 'verified']


class ChatMessageAdmin(admin.ModelAdmin):
    list_editable = ['is_read']
    list_display = ['sender', 'receiver', 'message', 'date', 'is_read']




admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)