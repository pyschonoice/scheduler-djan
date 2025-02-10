from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Employee(models.Model):
    STATUS_CHOICES = (
        ('probation', 'Probation'),
        ('full_time', 'Full Time'),
        ('rejected', 'Rejected'),
    )
    # Link to Django’s built-in user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # When the employee’s probation period ends
    probation_end_date = models.DateTimeField()
    # Current status of the employee
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='probation')
    # Whether an automated request has been sent to the employer
    is_request_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
