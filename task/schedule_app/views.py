# probation_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Employee


def home(request):
    return render(request, 'schedule_app/home.html',{})

def register(request):
    """
    Registration view for employee users.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionally create an Employee instance with default probation_end_date
            # For example, setting probation_end_date 30 days from now:
            Employee.objects.create(
                user=user,
                probation_end_date=timezone.now() + timezone.timedelta(days=30)
            )
            login(request, user)  # Log in the new user automatically.
            return redirect('employee_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'schedule_app/register.html', {'form': form})

def login_view(request):
    """
    Login view for employees.
    If the logged-in user is a superuser, redirect to the employer dashboard.
    """
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Retrieve the user from the form.
            login(request, user)
            # Redirect admin users to employer dashboard.
            if user.is_superuser:
                return redirect('employer_dashboard')
            return redirect('employee_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'schedule_app/login.html', {'form': form})

def logout_view(request):
   
    logout(request)
    return redirect('home')

@login_required
def employee_dashboard(request):
    """
    Display the logged-in employee's status and probation end date.
    This view is intended for employees.
    """
    employee = get_object_or_404(Employee, user=request.user)
    context = {
        'employee': employee,
        'now': timezone.now(),  # For template date comparisons
    }
    return render(request, 'schedule_app/employee_dashboard.html', context)

@login_required
def employer_dashboard(request):
    """
    List all employees for which an automated request has been sent (i.e. probation has ended).
    This view is intended for the employer (admin/superuser).
    """
    # Only allow access to superusers (the employer)
    if not request.user.is_superuser:
        return redirect('employee_dashboard')
    employees = Employee.objects.filter(status='probation', is_request_sent=True)
    context = {
        'employees': employees,
    }
    return render(request, 'schedule_app/employer_dashboard.html', context)

@require_POST
@login_required
def handle_decision(request, employee_id):
    """
    Handle the employer’s decision for an employee:
    - 'confirm': mark the employee as full-time.
    - 'reject': mark the employee as rejected.
    - 'extend': extend the probation period by a number of days.
    
    Only accessible by the employer (admin/superuser).
    """
    if not request.user.is_superuser:
        return redirect('employee_dashboard')
    
    employee = get_object_or_404(Employee, id=employee_id)
    action = request.POST.get('action')
    
    if action == 'confirm':
        employee.status = 'full_time'
        employee.save()
    elif action == 'reject':
        employee.status = 'rejected'
        employee.save()
    elif action == 'extend':
        try:
            extend_days = int(request.POST.get('extend_days', 0))
        except ValueError:
            extend_days = 0
        if extend_days > 0:
            # Extend probation_end_date by the specified number of days.
            employee.probation_end_date += timezone.timedelta(days=extend_days)
            # Reset the request flag so the new date is re‑checked.
            employee.is_request_sent = False
            employee.save()
    return redirect('employer_dashboard')
