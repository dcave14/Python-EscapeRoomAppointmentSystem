import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import EscapeRoom, Booking
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def create_booking(request, room_id):
    escape_room = get_object_or_404(EscapeRoom, id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        print("Submitted form data:")
        print(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = escape_room

            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']

            # Validate start and end times
            try:
                print("Parsed start_time:", start_time)
                print("Parsed end_time:", end_time)
            except ValueError:
                form.add_error('start_time', 'Enter a valid time.')
                form.add_error('end_time', 'Enter a valid time.')
            else:
                # Check if end time is after start time
                if end_time <= start_time:
                    form.add_error('end_time', 'End time must be after start time.')

            if not form.errors:
                # Validate availability and capacity
                if not is_available(booking):
                    messages.error(request, 'The selected time slot is not available.')
                    return redirect('booking:escape_room_detail', room_id=room_id)

                if booking.num_participants > escape_room.capacity:
                    messages.error(request, 'The number of participants exceeds the room capacity.')
                    return redirect('booking:escape_room_detail', room_id=room_id)

                # Validate fully booked days
                if is_fully_booked(booking.date):
                    messages.error(request, 'The selected day is fully booked.')
                    return redirect('booking:escape_room_detail', room_id=room_id)

                # Calculate total price
                booking.total_price = calculate_price(booking)

                booking.save()
                return redirect('booking:booking_confirmation', booking_id=booking.id)
        else:
            print("Form errors:", form.errors)
    else:
        form = BookingForm()

    context = {
        'escape_room': escape_room,
        'form': form,
    }
    return render(request, 'booking/escape_room_detail.html', context)

def is_available(booking):
    # Check if the selected date and time slot are available
    overlapping_bookings = Booking.objects.filter(
        room=booking.room,
        date=booking.date,
        start_time__lt=booking.end_time,
        end_time__gt=booking.start_time,
    )
    return not overlapping_bookings.exists()

def is_fully_booked(date):
    bookings = Booking.objects.filter(date=date)
    available_slots = EscapeRoom.objects.filter(availability=True).count() * 12
    booked_slots = bookings.count()
    return booked_slots >= available_slots

def calculate_price(booking):
    base_price = booking.room.price
    additional_cost_per_participant = 10
    total_price = base_price + (booking.num_participants * additional_cost_per_participant)
    return total_price

def escape_room_detail(request, room_id):
    escape_room = get_object_or_404(EscapeRoom, id=room_id)
    if escape_room.image and escape_room.image.url:
        print(escape_room.image.url)
    return render(request, 'booking/escape_room_detail.html', {'escape_room': escape_room})

def escape_room_list(request):
    rooms = EscapeRoom.objects.all()
    return render(request, 'booking/escape_room_list.html', {'escape_rooms': rooms})

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'booking/booking_confirmation.html', {'booking': booking})

def available_times(request, room_id):
    selected_date = request.GET.get('date')
    if not selected_date:
        return JsonResponse({"error": "No date provided"}, status=400)
    
    room = get_object_or_404(EscapeRoom, id=room_id)
    bookings = Booking.objects.filter(room=room, date=selected_date)
    occupied_times = [(booking.start_time, booking.end_time) for booking in bookings]

    all_times = [datetime.time(hour=h) for h in range(9, 21)]
    available_times = [time for time in all_times if all(not (booking[0] <= time < booking[1]) for booking in occupied_times)]

    return JsonResponse({"available_times": [time.strftime('%H:%M') for time in available_times]})

@login_required
def request_cancellation(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if booking.user == request.user:
        booking.cancellation_requested = True
        booking.save()
    return redirect('profile')