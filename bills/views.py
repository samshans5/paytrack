from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import BillForm, ReminderRuleForm, SignUpForm, UtilityForm
from .models import Bill, BillStatus, Notification, ReminderRule, Utility


class PayTrackLoginView(LoginView):
    template_name = "registration/login.html"


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. You can log in now.")
            return redirect("login")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def dashboard(request):
    today = timezone.localdate()
    upcoming_window = today + timedelta(days=14)

    bills = Bill.objects.filter(user=request.user).select_related("utility")
    pending_bills = bills.filter(status=BillStatus.PENDING).order_by("due_date")
    upcoming_bills = pending_bills.filter(due_date__lte=upcoming_window)
    overdue_bills = pending_bills.filter(due_date__lt=today)
    unread_notifications = Notification.objects.filter(
        user=request.user, is_read=False
    ).count()

    return render(
        request,
        "bills/dashboard.html",
        {
            "utilities_count": Utility.objects.filter(user=request.user, is_active=True).count(),
            "pending_count": pending_bills.count(),
            "overdue_count": overdue_bills.count(),
            "upcoming_bills": upcoming_bills[:5],
            "recent_notifications": Notification.objects.filter(user=request.user)[:5],
            "unread_notifications": unread_notifications,
        },
    )


@login_required
def utility_list(request):
    utilities = Utility.objects.filter(user=request.user)
    return render(request, "bills/utility_list.html", {"utilities": utilities})


@login_required
def utility_create(request):
    if request.method == "POST":
        form = UtilityForm(request.POST)
        if form.is_valid():
            utility = form.save(commit=False)
            utility.user = request.user
            utility.save()
            messages.success(request, f'Utility "{utility.name}" added.')
            return redirect("utility_list")
    else:
        form = UtilityForm()

    return render(request, "bills/utility_form.html", {"form": form, "title": "Add Utility"})


@login_required
def utility_edit(request, pk):
    utility = get_object_or_404(Utility, pk=pk, user=request.user)
    if request.method == "POST":
        form = UtilityForm(request.POST, instance=utility)
        if form.is_valid():
            form.save()
            messages.success(request, f'Utility "{utility.name}" updated.')
            return redirect("utility_list")
    else:
        form = UtilityForm(instance=utility)

    return render(
        request,
        "bills/utility_form.html",
        {"form": form, "title": "Edit Utility", "utility": utility},
    )


@login_required
@require_POST
def utility_delete(request, pk):
    utility = get_object_or_404(Utility, pk=pk, user=request.user)
    name = utility.name
    utility.delete()
    messages.success(request, f'Utility "{name}" removed.')
    return redirect("utility_list")


@login_required
def bill_list(request):
    status_filter = request.GET.get("status", "all")
    bills = Bill.objects.filter(user=request.user).select_related("utility")

    if status_filter == "pending":
        bills = bills.filter(status=BillStatus.PENDING)
    elif status_filter == "paid":
        bills = bills.filter(status=BillStatus.PAID)
    elif status_filter == "overdue":
        bills = bills.filter(status=BillStatus.PENDING, due_date__lt=timezone.localdate())

    return render(
        request,
        "bills/bill_list.html",
        {"bills": bills, "status_filter": status_filter},
    )


@login_required
def bill_create(request):
    if request.method == "POST":
        form = BillForm(request.user, request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.user = request.user
            bill.save()
            messages.success(request, "Bill added.")
            return redirect("bill_list")
    else:
        form = BillForm(request.user)

    return render(request, "bills/bill_form.html", {"form": form, "title": "Add Bill"})


@login_required
def bill_edit(request, pk):
    bill = get_object_or_404(Bill, pk=pk, user=request.user)
    if request.method == "POST":
        form = BillForm(request.user, request.POST, instance=bill)
        if form.is_valid():
            form.save()
            messages.success(request, "Bill updated.")
            return redirect("bill_list")
    else:
        form = BillForm(request.user, instance=bill)

    return render(
        request,
        "bills/bill_form.html",
        {"form": form, "title": "Edit Bill", "bill": bill},
    )


@login_required
@require_POST
def bill_mark_paid(request, pk):
    bill = get_object_or_404(Bill, pk=pk, user=request.user)
    bill.mark_paid()
    messages.success(request, f"{bill.utility.name} bill marked as paid.")
    return redirect(request.POST.get("next") or "bill_list")


@login_required
@require_POST
def bill_delete(request, pk):
    bill = get_object_or_404(Bill, pk=pk, user=request.user)
    bill.delete()
    messages.success(request, "Bill deleted.")
    return redirect("bill_list")


@login_required
def reminder_list(request):
    rules = ReminderRule.objects.filter(user=request.user).select_related("utility")
    return render(request, "bills/reminder_list.html", {"rules": rules})


@login_required
def reminder_create(request):
    if request.method == "POST":
        form = ReminderRuleForm(request.user, request.POST)
        if form.is_valid():
            rule = form.save(commit=False)
            rule.user = request.user
            rule.save()
            messages.success(request, "Reminder rule created.")
            return redirect("reminder_list")
    else:
        form = ReminderRuleForm(request.user)

    return render(
        request,
        "bills/reminder_form.html",
        {"form": form, "title": "Add Reminder Rule"},
    )


@login_required
def reminder_edit(request, pk):
    rule = get_object_or_404(ReminderRule, pk=pk, user=request.user)
    if request.method == "POST":
        form = ReminderRuleForm(request.user, request.POST, instance=rule)
        if form.is_valid():
            form.save()
            messages.success(request, "Reminder rule updated.")
            return redirect("reminder_list")
    else:
        form = ReminderRuleForm(request.user, instance=rule)

    return render(
        request,
        "bills/reminder_form.html",
        {"form": form, "title": "Edit Reminder Rule", "rule": rule},
    )


@login_required
@require_POST
def reminder_delete(request, pk):
    rule = get_object_or_404(ReminderRule, pk=pk, user=request.user)
    rule.delete()
    messages.success(request, "Reminder rule deleted.")
    return redirect("reminder_list")


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).select_related("bill")
    return render(
        request,
        "bills/notification_list.html",
        {"notifications": notifications},
    )


@login_required
@require_POST
def notification_mark_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save(update_fields=["is_read"])
    return redirect("notification_list")


@login_required
@require_POST
def notification_mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, "All notifications marked as read.")
    return redirect("notification_list")
