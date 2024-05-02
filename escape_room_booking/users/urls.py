from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('request_cancellation/<int:booking_id>/', views.request_cancellation, name='request_cancellation'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html', next_page='home'), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)