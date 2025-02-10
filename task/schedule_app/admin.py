from django.contrib import admin
from .models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view.
    list_display = ('user', 'probation_end_date', 'status', 'is_request_sent')
    
    # Allow filtering by status and request flag.
    list_filter = ('status', 'is_request_sent')
    
    # Enable searching by the username of the related user.
    search_fields = ('user__username',)
    
    # Specify the fields to display/edit on the change form.
    fields = ('user', 'probation_end_date', 'status', 'is_request_sent')
    
    # Order the list by probation_end_date by default.
    ordering = ('probation_end_date',)

# Register the Employee model with our custom ModelAdmin.
admin.site.register(Employee, EmployeeAdmin)
