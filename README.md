# PayTrack

Utility bill payment tracker with custom utilities, due-date reminders, and in-app notifications.

## Features

- **Custom utilities** — Add electricity, water, gas, internet, rent, or any custom bill type
- **Bill tracking** — Record amounts, due dates, and mark bills as paid
- **Reminder rules** — Configure alerts N days before a bill is due (per utility or globally)
- **Notifications** — In-app notification center; optional email via `--send-email`
- **Dashboard** — Overview of upcoming, pending, and overdue bills

## Quick start

```powershell
cd C:\Users\shanm\paytrack
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/, sign up, then:

1. Add your utilities
2. Add bills with due dates
3. Create reminder rules (e.g. 7, 3, and 1 day before due)
4. Run reminders daily:

```powershell
python manage.py send_reminders
python manage.py send_reminders --send-email
```

Schedule `send_reminders` with Windows Task Scheduler or cron in production.

## Project structure

```
paytrack/
├── bills/              # Main app (models, views, reminders)
├── config/             # Django settings & URLs
├── templates/          # HTML templates
├── static/             # CSS
└── manage.py
```

## Environment variables (optional)

Create a `.env` file:

```
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

## Admin

Django admin is available at `/admin/` after creating a superuser.

## Next steps

- Add recurring bill templates (auto-generate monthly bills)
- SMS/push notifications (Twilio, Firebase)
- REST API with Django REST Framework or a FastAPI microservice
- Multi-currency support
