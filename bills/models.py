from django.conf import settings
from django.db import models
from django.utils import timezone


class UtilityCategory(models.TextChoices):
    ELECTRICITY = "electricity", "Electricity"
    MOBILE_RECHARGE = "mobile_recharge", "Mobile Recharge"
    FASTAG_RECHARGE = "fastag_recharge", "Fastag Recharge"
    WATER = "water", "Water"
    GAS = "gas", "Gas"
    INTERNET = "internet", "Internet"
    PHONE = "phone", "Phone"
    RENT = "rent", "Rent"
    CREDIT_CARD = "credit_card", "Credit Card"
    CUSTOM = "custom", "Custom"


class Utility(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="utilities",
    )
    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20,
        choices=UtilityCategory,
        default=UtilityCategory.CUSTOM,
    )
    provider = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "utilities"

    def __str__(self):
        return self.name


class BillStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    OVERDUE = "overdue", "Overdue"


class Bill(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bills",
    )
    utility = models.ForeignKey(
        Utility,
        on_delete=models.CASCADE,
        related_name="bills",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    billing_period_start = models.DateField(null=True, blank=True)
    billing_period_end = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=BillStatus,
        default=BillStatus.PENDING,
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["due_date", "-created_at"]

    def __str__(self):
        return f"{self.utility.name} — ₹{self.amount} due {self.due_date}"

    @property
    def is_overdue(self):
        return self.status == BillStatus.PENDING and self.due_date < timezone.localdate()

    def mark_paid(self):
        self.status = BillStatus.PAID
        self.paid_at = timezone.now()
        self.save(update_fields=["status", "paid_at"])


class ReminderRule(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reminder_rules",
    )
    utility = models.ForeignKey(
        Utility,
        on_delete=models.CASCADE,
        related_name="reminder_rules",
        null=True,
        blank=True,
        help_text="Leave blank to apply to all utilities.",
    )
    days_before_due = models.PositiveSmallIntegerField(default=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-days_before_due"]
        unique_together = [("user", "utility", "days_before_due")]

    def __str__(self):
        target = self.utility.name if self.utility else "All utilities"
        return f"{target}: {self.days_before_due} day(s) before due"


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
