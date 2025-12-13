from django.contrib import admin
from .models import ParkingSlot, ParkingSession


@admin.register(ParkingSlot)
class ParkingSlotAdmin(admin.ModelAdmin):
    list_display = ("code", "floor", "is_occupied")
    list_filter = ("floor", "is_occupied")
    search_fields = ("code",)


@admin.register(ParkingSession)
class ParkingSessionAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_number",
        "plate_number",
        "slot",
        "status",
        "time_in",
        "time_out",
        "amount_due",
        "cash_received",
        "amount_paid",
        "change",
    )
    list_filter = ("status", "slot__floor")
    search_fields = ("ticket_number", "plate_number", "slot__code")
    ordering = ("-time_in",)
