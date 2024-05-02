from django.db import models
from django.contrib.auth.models import User

class EscapeRoom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.IntegerField()  # Changed from CharField to IntegerField
    duration = models.IntegerField()
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='room_images/', null=True, blank=True)
    availability = models.BooleanField(default=True)  # Adjust the field type as needed

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(EscapeRoom, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    num_participants = models.IntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancellation_requested = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.room.name} - {self.date}"