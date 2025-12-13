from decimal import Decimal
from django import forms
from .models import ParkingSlot


class CheckInForm(forms.Form):
    plate_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        "placeholder": "Enter plate number",
        "class": "input",
        "autocomplete": "off",
    }))
    slot = forms.ModelChoiceField(
        queryset=ParkingSlot.objects.filter(is_occupied=False),
        empty_label="Select parking slot",
        widget=forms.Select(attrs={"class": "input"}),
    )


class CheckOutForm(forms.Form):
    plate_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        "placeholder": "Enter plate number",
        "class": "input",
        "autocomplete": "off",
    }))
    cash_received = forms.DecimalField(min_value=Decimal("0.00"), decimal_places=2, max_digits=10, widget=forms.NumberInput(attrs={
        "placeholder": "Cash received",
        "class": "input",
        "step": "0.01",
    }))
