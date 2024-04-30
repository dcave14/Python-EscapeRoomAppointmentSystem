from django.contrib import admin
from .models import EscapeRoom, Booking

@admin.register(EscapeRoom)
class EscapeRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'theme', 'difficulty', 'duration', 'price')
    list_filter = ('theme', 'difficulty')
    search_fields = ('name', 'description')
    
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'date', 'time_slot', 'num_participants', 'total_price')
    list_filter = ('date', 'room')
    search_fields = ('user__username', 'room__name')