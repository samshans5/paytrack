from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Bill, ReminderRule, Utility


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class UtilityForm(forms.ModelForm):
    class Meta:
        model = Utility
        fields = ("name", "category", "provider", "account_number", "notes", "is_active")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. City Power & Light"}),
            "provider": forms.TextInput(attrs={"placeholder": "Utility company name"}),
            "account_number": forms.TextInput(attrs={"placeholder": "Optional account #"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = (
            "utility",
            "amount",
            "due_date",
            "billing_period_start",
            "billing_period_end",
            "notes",
        )
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "billing_period_start": forms.DateInput(attrs={"type": "date"}),
            "billing_period_end": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["utility"].queryset = Utility.objects.filter(user=user, is_active=True)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class ReminderRuleForm(forms.ModelForm):
    class Meta:
        model = ReminderRule
        fields = ("utility", "days_before_due", "is_active")
        widgets = {
            "days_before_due": forms.NumberInput(attrs={"min": 1, "max": 60}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["utility"].queryset = Utility.objects.filter(user=user, is_active=True)
        self.fields["utility"].required = False
        self.fields["utility"].empty_label = "All utilities"
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

    def clean_days_before_due(self):
        days = self.cleaned_data["days_before_due"]
        if days < 1:
            raise forms.ValidationError("Reminders must be at least 1 day before the due date.")
        return days
