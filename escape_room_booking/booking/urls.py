from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'booking'

urlpatterns = [
    path('escape-rooms/', views.escape_room_list, name='escape_room_list'),
    path('escape-rooms/<int:room_id>/', views.escape_room_detail, name='escape_room_detail'),
    path('escape-rooms/<int:room_id>/book/', views.create_booking, name='create_booking'),
    path('bookings/<int:booking_id>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)