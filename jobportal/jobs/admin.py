from django.contrib import admin
from .models import Job, Application, Profile

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'posted_by', 'created_at')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'applied_at')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
