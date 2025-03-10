"""
URL configuration for omniartiste project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from pages import views 

urlpatterns = [
    path('invoices/', views.invoices, name='invoices'),  # Dashboard URL
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('sitemap', views.sitemap, name='sitemap'),
    path('contact', views.contact, name='contact'),
    path('events', views.events, name='events'),
    path('buy-now/<uuid:event_id>', views.buy_now, name='buy_now'),
    path('verify-email', views.verify_email, name='verify_email'),
    path('payment-success', views.payment_successful, name='payment_successful'),
    path('payment-failure', views.payment_failure, name='payment_failure'),
    path('ticket-verification-failure', views.ticket_verification_failure, name='ticket_verification_failure'),
    path('payment-for-tickets', views.payment_for_tickets, name='payment_for_tickets'),
    path('email_verification_success', views.email_verification_success, name='email_verification_success'),
    path('jobs', views.jobs, name='jobs'),
    path('jobs/<uuid:job_id>', views.jobDetail, name='jobDetail'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='forgot_password.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
