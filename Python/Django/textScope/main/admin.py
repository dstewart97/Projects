from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import Topic


admin.site.register(Topic)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'expire_date']