# FILEPATH: /f:/COLLEGE/SEMESTER 5/PYTHON II/FINAL PROJECT/Python-EscapeRoomAppointmentSystem/escape_room_booking/users/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserUpdateForm

class UserRegistrationFormTest(TestCase):

    def test_form_with_valid_data(self):
        form = UserRegistrationForm({
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertTrue(form.is_valid())

    def test_form_with_invalid_data(self):
        form = UserRegistrationForm({
            'username': '',
            'email': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertFalse(form.is_valid())

class UserUpdateFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )

    def test_form_with_valid_data(self):
        form = UserUpdateForm({
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
        }, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_form_with_invalid_data(self):
        form = UserUpdateForm({
            'username': '',
            'email': 'updateduser@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
        }, instance=self.user)
        self.assertFalse(form.is_valid())