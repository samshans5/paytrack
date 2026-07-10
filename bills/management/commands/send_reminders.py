from datetime import timedelta

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from bills.models import Bill, BillStatus, Notification, ReminderRule


class Command(BaseCommand):
    help = "Send bill payment reminders based on user reminder rules."

    def add_arguments(self, parser):
        parser.add_argument(
            "--send-email",
            action="store_true",
            help="Also send email notifications (requires email backend configured).",
        )

    def handle(self, *args, **options):
        today = timezone.localdate()
        sent_count = 0

        rules = ReminderRule.objects.filter(is_active=True).select_related("user", "utility")

        for rule in rules:
            reminder_date = today + timedelta(days=rule.days_before_due)
            bills = Bill.objects.filter(
                user=rule.user,
                status=BillStatus.PENDING,
                due_date=reminder_date,
            ).select_related("utility")

            if rule.utility_id:
                bills = bills.filter(utility=rule.utility)

            for bill in bills:
                title = f"Bill due in {rule.days_before_due} day(s): {bill.utility.name}"
                message = (
                    f"Your {bill.utility.name} bill of ₹{bill.amount} "
                    f"is due on {bill.due_date:%b %d, %Y}."
                )

                already_sent = Notification.objects.filter(
                    user=rule.user,
                    bill=bill,
                    title=title,
                    created_at__date=today,
                ).exists()

                if already_sent:
                    continue

                Notification.objects.create(
                    user=rule.user,
                    bill=bill,
                    title=title,
                    message=message,
                )
                sent_count += 1

                if options["send_email"] and rule.user.email:
                    send_mail(
                        subject=title,
                        message=message,
                        from_email=None,
                        recipient_list=[rule.user.email],
                        fail_silently=True,
                    )

        self.stdout.write(self.style.SUCCESS(f"Created {sent_count} reminder notification(s)."))
