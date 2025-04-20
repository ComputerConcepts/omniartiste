from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_email, name='admin_login_email'),
    path('login/password/', views.login_password, name='admin_login_password'),
    path('dashboard/', views.dashboard, name='admin_dashboard'),
    path('jobs/', views.jobs_view, name='admin_jobs'),
    path('events/', views.events_view, name='admin_events'),
    path('invoices/', views.invoices_view, name='admin_invoices'),
    path('logout/', views.admin_logout, name='admin_logout'),  # optional but good to have
    path('reset-password/', views.reset_password_view, name='admin_reset_password'),
]
