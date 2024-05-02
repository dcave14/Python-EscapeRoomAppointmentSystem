from django.contrib import admin
from .models import EscapeRoom, Booking

@admin.register(EscapeRoom)
class EscapeRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'duration', 'price')
    search_fields = ('name', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'date', 'start_time', 'end_time', 'num_participants', 'total_price', 'cancellation_requested')
    list_filter = ('date', 'room', 'cancellation_requested')
    search_fields = ('user__username', 'room__name')