from django.test import TestCase
from django.contrib.auth.models import User
from .models import Booking, EscapeRoom

class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.room = EscapeRoom.objects.create(name='Test Room', description='Test Room', difficulty=1, duration=60, capacity=5, price=100.00, availability=True)
        self.booking = Booking.objects.create(user=self.user, room=self.room, date='2022-12-31', start_time='10:00:00', end_time='11:00:00', num_participants=5, total_price=500.00)

    def test_booking_content(self):
        self.assertEqual(f'{self.booking.user.username}', 'testuser')
        self.assertEqual(f'{self.booking.room.name}', 'Test Room')
        self.assertEqual(f'{self.booking.date}', '2022-12-31')
        self.assertEqual(f'{self.booking.start_time}', '10:00:00')
        self.assertEqual(f'{self.booking.end_time}', '11:00:00')
        self.assertEqual(self.booking.num_participants, 5)
        self.assertEqual(self.booking.total_price, 500.00)
        self.assertEqual(self.booking.cancellation_requested, False)
        
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Booking, EscapeRoom

class RequestCancellationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.room = EscapeRoom.objects.create(name='Test Room', description='Test Room', difficulty=1, duration=60, capacity=5, price=100.00, availability=True)
        self.booking = Booking.objects.create(user=self.user, room=self.room, date='2022-12-31', start_time='10:00:00', end_time='11:00:00', num_participants=5, total_price=500.00)

    def test_request_cancellation(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(f'/booking/request_cancellation/{self.booking.id}/')
        self.booking.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.booking.cancellation_requested)
        
        
from django.test import TestCase
from .forms import BookingForm
from datetime import datetime, time

class TestBookingForm(TestCase):
    def setUp(self):
        self.valid_data = {
            'date': datetime.now().date(),
            'start_time': time(hour=10, minute=0),
            'end_time': time(hour=11, minute=0),
            'num_participants': 5
        }

    def test_form_valid(self):
        form = BookingForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
