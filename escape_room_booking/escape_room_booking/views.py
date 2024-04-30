from django.shortcuts import render

def home(request):
    return render(request, 'escape_room_booking/home.html')