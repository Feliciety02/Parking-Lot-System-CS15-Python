from django import forms
from decimal import Decimal
from .models import ParkingSlot, ParkingSession


class CheckInForm(forms.Form):
    plate_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter plate number",
            "class": "input",
            "autocomplete": "off",
        })
    )
    slot = forms.ModelChoiceField(
        queryset=ParkingSlot.objects.filter(is_occupied=False),
        empty_label="Select parking slot",
        widget=forms.Select(attrs={"class": "input"}),
    )


class CheckOutForm(forms.Form):
    session = forms.ModelChoiceField(
        queryset=ParkingSession.objects.filter(status=ParkingSession.STATUS_ACTIVE),
        empty_label="Select a parked vehicle",
        label="Parked vehicle",
        widget=forms.Select(attrs={"class": "input"})
    )

    cash_received = forms.DecimalField(
        min_value=Decimal("0.00"),
        decimal_places=2,
        label="Cash received",
        required=False,
        widget=forms.NumberInput(attrs={
            "class": "input",
            "placeholder": "Enter cash amount"
        })
    )
