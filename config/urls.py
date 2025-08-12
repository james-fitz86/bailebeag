"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path

from . import views
from users import views as user_views
from django.contrib.auth import views as auth_views
from bookings import views as booking_views
from teams import views as team_views
from alerts import views as alert_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    path('profile/', user_views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('bookings/new/', booking_views.create_booking, name='create_booking'),
    path('bookings/', booking_views.BookingList.as_view(), name='booking_list'),
    path('bookings/<int:pk>', booking_views.BookingDetail.as_view(), name='booking_detail'),
    path('bookings/<int:pk>/update/', booking_views.BookingUpdateView.as_view(template_name='bookings/create_booking.html'), name='booking_update'),
    path('bookings/<int:pk>/delete/', booking_views.BookingDeleteView.as_view(), name='booking_delete'),
    path('bookings/<int:booking_id>/approve/', booking_views.approve_booking, name='booking_approve'),
    path('bookings/<int:booking_id>/reject/', booking_views.reject_booking, name='booking_reject'),
    path('pitches/', booking_views.PitchList.as_view(), name='pitch_list'),
    path('teams/create/', team_views.create_team, name='create_team'),
    path('teams/', team_views.TeamList.as_view(), name='team_list'),
    path('teams/<int:pk>/', team_views.TeamDetail.as_view(), name='team_detail'),
    path('teams/<int:pk>/edit/', team_views.TeamUpdateView.as_view(), name='team_edit'),
    path('teams/<int:pk>/delete/', team_views.TeamDeleteView.as_view(), name='team_delete'),
    path('notifications/', alert_views.NotificationListView.as_view(), name='notification_list'),
    path('notifications/<int:pk>/', alert_views.NotificationDetailView.as_view(), name='notification_detail'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html', html_email_template_name='users/emails/password_reset_email.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),

]
