from django.urls import path
from .views import register, activate, user_login, user_logout
from django.contrib.auth import views as auth_views


urlpatterns = [
   path('register/', register, name='register'),
   path('activate/<uidb64>/<token>/', activate, name='activate'),
   path('login/', user_login, name='login'),
   path('logout/', user_logout, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
]
