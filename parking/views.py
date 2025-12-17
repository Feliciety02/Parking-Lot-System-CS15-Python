from decimal import Decimal
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CheckInForm, CheckOutForm
from .models import ParkingSession, ParkingSlot, RATE_PER_HOUR


def dashboard(request):
    active_sessions = ParkingSession.objects.filter(
        status=ParkingSession.STATUS_ACTIVE
    ).select_related("slot")

    paid_sessions = ParkingSession.objects.filter(
        status=ParkingSession.STATUS_PAID
    ).select_related("slot")

    return render(request, "parking/home.html", {
        "active_sessions": active_sessions,
        "paid_sessions": paid_sessions,
        "rate_per_hour": RATE_PER_HOUR,
        "available_slots": ParkingSlot.objects.filter(is_occupied=False).count(),
        "occupied_slots": ParkingSlot.objects.filter(is_occupied=True).count(),
        "total_slots": ParkingSlot.objects.count(),
    })


@transaction.atomic
def check_in(request):
    if request.method == "POST":
        form = CheckInForm(request.POST)
        if form.is_valid():
            slot = form.cleaned_data["slot"]
            slot = ParkingSlot.objects.select_for_update().get(pk=slot.pk)

            if slot.is_occupied:
                form.add_error("slot", "This parking slot is already occupied.")
            else:
                plate = form.cleaned_data["plate_number"].strip().upper()

                if ParkingSession.objects.filter(
                    plate_number=plate,
                    status=ParkingSession.STATUS_ACTIVE
                ).exists():
                    form.add_error("plate_number", "This plate number is already parked.")
                else:
                    slot.is_occupied = True
                    slot.save()

                    ParkingSession.objects.create(
                        ticket_number=ParkingSession.generate_ticket_number(),
                        plate_number=plate,
                        slot=slot,
                        time_in=timezone.now(),
                        status=ParkingSession.STATUS_ACTIVE,
                    )

                    messages.success(request, f"Checked in {plate} at slot {slot.code}")
                    return redirect("dashboard")
    else:
        form = CheckInForm()

    return render(request, "parking/check_in.html", {"form": form})


@transaction.atomic
def check_out(request):
    form = CheckOutForm(request.POST or None)

    context = {
        "form": form,
        "rate_per_hour": RATE_PER_HOUR,
    }

    if request.method == "POST" and form.is_valid():
        session = form.cleaned_data["session"]
        cash = form.cleaned_data.get("cash_received")

        session = ParkingSession.objects.select_for_update().select_related("slot").get(
            pk=session.pk
        )

        session.time_out = timezone.now()
        amount_due = session.compute_amount_due()
        hours = session.billed_hours()

        context.update({
            "session": session,
            "hours": hours,
            "amount_due": amount_due,
        })

        if cash is not None:
            try:
                session.checkout_and_pay_full(Decimal(cash))
            except ValueError as e:
                form.add_error(None, str(e))
                return render(request, "parking/check_out.html", context)

            session.save()

            slot = session.slot
            slot.is_occupied = False
            slot.save()

            messages.success(
                request,
                f"Paid ₱{session.amount_paid:.2f}. "
                f"Change ₱{session.change:.2f}. "
                f"Slot {slot.code} is now available."
            )

            return redirect("session_detail", session_id=session.id)

    return render(request, "parking/check_out.html", context)


def session_detail(request, session_id):
    session = get_object_or_404(
        ParkingSession.objects.select_related("slot"),
        pk=session_id
    )

    return render(request, "parking/session_detail.html", {
        "session": session,
        "rate_per_hour": RATE_PER_HOUR
    })
