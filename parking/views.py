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
    available_slots = ParkingSlot.objects.filter(
        is_occupied=False
    ).order_by("floor", "code")

    if request.method == "POST":
        form = CheckInForm(request.POST)
        if form.is_valid():
            slot = ParkingSlot.objects.select_for_update().get(
                pk=form.cleaned_data["slot"].pk
            )

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

                    messages.success(
                        request,
                        f"Checked in {plate} at slot {slot.code}"
                    )
                    return redirect("dashboard")
    else:
        form = CheckInForm()

    return render(request, "parking/check_in.html", {
        "form": form,
        "available_slots": available_slots,
    })


@transaction.atomic
def check_out(request):
    active_sessions = ParkingSession.objects.filter(
        status=ParkingSession.STATUS_ACTIVE
    ).select_related("slot")

    selected_session = None
    amount_due = None
    hours = None

    if request.method == "POST":
        form = CheckOutForm(request.POST)

        if form.is_valid():
            session_id = form.cleaned_data["session"]
            cash = form.cleaned_data.get("cash_received")

            selected_session = ParkingSession.objects.select_for_update().get(
                pk=session_id,
                status=ParkingSession.STATUS_ACTIVE
            )

            selected_session.time_out = timezone.now()
            hours = selected_session.billed_hours()
            amount_due = selected_session.compute_amount_due()

            if cash is not None:
                try:
                    selected_session.checkout_and_pay_full(Decimal(cash))
                except ValueError as e:
                    form.add_error(None, str(e))
                else:
                    selected_session.save()

                    slot = selected_session.slot
                    slot.is_occupied = False
                    slot.save()

                    messages.success(
                        request,
                        f"Paid ₱{selected_session.amount_paid:.2f}. "
                        f"Change ₱{selected_session.change:.2f}."
                    )
                    return redirect("session_detail", session_id=selected_session.id)
    else:
        form = CheckOutForm()

    return render(request, "parking/check_out.html", {
        "form": form,
        "active_sessions": active_sessions,
        "selected_session": selected_session,
        "amount_due": amount_due,
        "hours": hours,
        "rate_per_hour": RATE_PER_HOUR,
    })


def session_detail(request, session_id):
    session = get_object_or_404(
        ParkingSession.objects.select_related("slot"),
        pk=session_id
    )

    # REALTIME COMPUTATION
    if session.status == ParkingSession.STATUS_ACTIVE:
        duration_minutes = session.duration_minutes()
        billed_hours = session.billed_hours()
        amount_due = session.compute_amount_due()
    else:
        duration_minutes = session.duration_minutes()
        billed_hours = session.billed_hours()
        amount_due = session.amount_due

    return render(request, "parking/session_detail.html", {
        "session": session,
        "rate_per_hour": RATE_PER_HOUR,
        "duration_minutes": duration_minutes,
        "billed_hours": billed_hours,
        "amount_due": amount_due,
    })
