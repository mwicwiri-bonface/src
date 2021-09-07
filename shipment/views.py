from django.shortcuts import render
from django.views.generic import ListView

from finance.models import Finance


class Home(ListView):
    model = Finance
    template_name = "shipment/index.html"
