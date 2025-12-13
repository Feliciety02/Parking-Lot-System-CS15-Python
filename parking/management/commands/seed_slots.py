from django.core.management.base import BaseCommand
from parking.models import ParkingSlot


class Command(BaseCommand):
    help = "Create parking slots A1-A6, B1-B6, C1-C6"

    def handle(self, *args, **options):
        created = 0
        for floor in ["A", "B", "C"]:
            for i in range(1, 7):
                code = f"{floor}{i}"
                _, was_created = ParkingSlot.objects.get_or_create(
                    code=code,
                    defaults={"floor": floor, "is_occupied": False},
                )
                if was_created:
                    created += 1
        self.stdout.write(self.style.SUCCESS(f"Seed complete. Created {created} slots."))
