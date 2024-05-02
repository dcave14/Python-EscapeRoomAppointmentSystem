from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import EscapeRoom, Booking
from .forms import BookingForm

def create_booking(request, room_id):
    escape_room = get_object_or_404(EscapeRoom, id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.escape_room = escape_room
            
            # Validate availability and capacity
            if not is_available(booking):
                messages.error(request, 'The selected time slot is not available.')
                return redirect('booking:escape_room_detail', room_id=room_id)
            
            if booking.num_participants > escape_room.capacity:
                messages.error(request, 'The number of participants exceeds the room capacity.')
                return redirect('booking:escape_room_detail', room_id=room_id)
            
            # Calculate total price
            booking.total_price = calculate_price(booking)
            
            booking.save()
            return redirect('booking:booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()
    
    context = {
        'escape_room': escape_room,
        'form': form,
    }
    return render(request, 'booking/escape_room_detail.html', context)

def is_available(booking):
    # Check if the selected date and time slot are available
    current_datetime = timezone.now()
    if booking.date < current_datetime.date():
        return False
    
    overlapping_bookings = Booking.objects.filter(
        escape_room=booking.escape_room,
        date=booking.date,
        time_slot=booking.time_slot,
    )
    return not overlapping_bookings.exists()

def calculate_price(booking):
    # Calculate the total price based on duration and number of participants
    base_price = booking.escape_room.price
    additional_cost_per_participant = 10
    total_price = base_price + (booking.num_participants * additional_cost_per_participant)
    return total_price

def escape_room_detail(request, room_id):
    escape_room = get_object_or_404(EscapeRoom, id=room_id)
    print(escape_room.image.url)  # Print the image URL
    return render(request, 'booking/escape_room_detail.html', {'escape_room': escape_room})

def escape_room_list(request):
    rooms = EscapeRoom.objects.all()  # Fetches all EscapeRoom objects from the database
    return render(request, 'booking/escape_room_list.html', {'escape_rooms': rooms})

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'booking/booking_confirmation.html', {'booking': booking})