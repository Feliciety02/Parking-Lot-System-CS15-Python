from __future__ import annotations

from decimal import Decimal
from math import ceil
from django.db import models
from django.utils import timezone

RATE_PER_HOUR = Decimal("30.00")


class ParkingSlot(models.Model):
    FLOOR_CHOICES = [
        ("A", "First floor"),
        ("B", "Second floor"),
        ("C", "Third floor"),
    ]

    floor = models.CharField(max_length=1, choices=FLOOR_CHOICES)
    code = models.CharField(max_length=5, unique=True)
    is_occupied = models.BooleanField(default=False)

    class Meta:
        ordering = ["code"]

    def __str__(self) -> str:
        return self.code


class ParkingSession(models.Model):
    STATUS_ACTIVE = "ACTIVE"
    STATUS_PAID = "PAID"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_PAID, "Paid"),
    ]

    ticket_number = models.CharField(max_length=32, unique=True)
    plate_number = models.CharField(max_length=20)
    slot = models.ForeignKey(ParkingSlot, on_delete=models.PROTECT, related_name="sessions")

    time_in = models.DateTimeField(default=timezone.now)
    time_out = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_ACTIVE)

    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    cash_received = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    change = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        ordering = ["-time_in"]

    def duration_minutes(self) -> int:
        end = self.time_out or timezone.now()
        seconds = (end - self.time_in).total_seconds()
        return int(ceil(seconds / 60)) if seconds > 0 else 0

    def billed_hours(self) -> int:
        minutes = self.duration_minutes()
        hours = (minutes + 59) // 60
        return max(hours, 1)

    def compute_amount_due(self) -> Decimal:
        return Decimal(self.billed_hours()) * RATE_PER_HOUR

    @staticmethod
    def generate_ticket_number() -> str:
        now = timezone.localtime()
        stamp = now.strftime("%Y%m%d-%H%M%S")
        rand = "".join("ABCDEFGHJKLMNPQRSTUVWXYZ23456789"[i % 32] for i in [
            now.microsecond % 32,
            (now.microsecond // 7) % 32,
            (now.microsecond // 13) % 32,
            (now.microsecond // 29) % 32,
        ])
        return f"PK-{stamp}-{rand}"

    def checkout_and_pay_full(self, cash: Decimal) -> None:
        if cash is None or cash <= 0:
            raise ValueError("Cash must be greater than 0")

        self.time_out = timezone.now()
        due = self.compute_amount_due()

        if cash < due:
            raise ValueError("Insufficient cash")

        self.amount_due = due
        self.cash_received = cash
        self.amount_paid = due
        self.change = cash - due
        self.status = self.STATUS_PAID

    def __str__(self) -> str:
        return f"{self.plate_number} {self.ticket_number}"
