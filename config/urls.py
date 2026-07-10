from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from bills.views import PayTrackLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("bills.urls")),
    path("login/", PayTrackLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
