from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("signup/", views.signup, name="signup"),
    path("utilities/", views.utility_list, name="utility_list"),
    path("utilities/add/", views.utility_create, name="utility_create"),
    path("utilities/<int:pk>/edit/", views.utility_edit, name="utility_edit"),
    path("utilities/<int:pk>/delete/", views.utility_delete, name="utility_delete"),
    path("bills/", views.bill_list, name="bill_list"),
    path("bills/add/", views.bill_create, name="bill_create"),
    path("bills/<int:pk>/edit/", views.bill_edit, name="bill_edit"),
    path("bills/<int:pk>/pay/", views.bill_mark_paid, name="bill_mark_paid"),
    path("bills/<int:pk>/delete/", views.bill_delete, name="bill_delete"),
    path("reminders/", views.reminder_list, name="reminder_list"),
    path("reminders/add/", views.reminder_create, name="reminder_create"),
    path("reminders/<int:pk>/edit/", views.reminder_edit, name="reminder_edit"),
    path("reminders/<int:pk>/delete/", views.reminder_delete, name="reminder_delete"),
    path("notifications/", views.notification_list, name="notification_list"),
    path(
        "notifications/<int:pk>/read/",
        views.notification_mark_read,
        name="notification_mark_read",
    ),
    path(
        "notifications/read-all/",
        views.notification_mark_all_read,
        name="notification_mark_all_read",
    ),
]
