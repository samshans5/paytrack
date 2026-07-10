from django.contrib import admin

from .models import Bill, Notification, ReminderRule, Utility


@admin.register(Utility)
class UtilityAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "category", "provider", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "provider", "user__username")


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ("utility", "user", "amount", "due_date", "status", "paid_at")
    list_filter = ("status", "due_date")
    search_fields = ("utility__name", "user__username")


@admin.register(ReminderRule)
class ReminderRuleAdmin(admin.ModelAdmin):
    list_display = ("user", "utility", "days_before_due", "is_active")
    list_filter = ("is_active",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "is_read", "created_at")
    list_filter = ("is_read",)
