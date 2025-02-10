
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('employee/', views.employee_dashboard, name='employee_dashboard'),
    path('employer/', views.employer_dashboard, name='employer_dashboard'),
    path('handle_decision/<int:employee_id>/', views.handle_decision, name='handle_decision'),
]
