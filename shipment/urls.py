from django.urls import path

from user.decorators import manager_required
from . import views

urlpatterns = [
    path('', manager_required(views.Home.as_view()), name="index"),
]
