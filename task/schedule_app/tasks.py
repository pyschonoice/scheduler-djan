from celery import shared_task
from django.utils import timezone
from .models import Employee

@shared_task
def check_probation_periods():
    """
    This task checks for employees still on probation whose probation_end_date
    has passed and who have not yet had a request sent to the employer.
    """
    now = timezone.now()
    # Find employees who are still in probation, their probation end date has passed, and no notification sent yet.
    employees = Employee.objects.filter(status='probation', probation_end_date__lte=now, is_request_sent=False)
    for employee in employees:
        # Mark that a request has been sent.
        employee.is_request_sent = True
        employee.save()
        # In a production app, you might send an email or create a notification.
        print(f"Probation period ended for {employee.user.username}. Notification sent to employer.")


# To run celery worker celery -A task worker --loglevel=info
# For windows use this so as to use less cpu : celery -A task worker --pool=solo --loglevel=info 
# To run celery beat celery -A task beat --loglevel=info

