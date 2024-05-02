from django.core.management.base import BaseCommand
from booking.models import EscapeRoom

class Command(BaseCommand):
    help = 'Preloads initial escape room data into the database'

    def handle(self, *args, **options):
        # Check if any EscapeRoom data already exists to prevent duplicate entries
        if EscapeRoom.objects.exists():
            self.stdout.write(self.style.WARNING('Initial data already loaded!'))
        else:
            # Data to preload
            rooms = [
                EscapeRoom(name="Pirate's Cove", description="Find the hidden treasure before time runs out.", difficulty=5, capacity=5, duration=60, price=25.00),
                EscapeRoom(name="Haunted Mansion", description="Escape the ghosts that haunt this creepy old house.", difficulty=7, capacity=6, duration=60, price=30.00)
            ]
            EscapeRoom.objects.bulk_create(rooms)
            self.stdout.write(self.style.SUCCESS('Successfully loaded initial data'))
