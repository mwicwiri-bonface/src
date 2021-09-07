from django.shortcuts import render
from django.views.generic import ListView

from salonist.models import Salonist
from service.models import Service
from store.models import Product, Order
from django.db.models import Q


class Home(ListView):
    model = Service
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.object_list.filter(is_active=True, is_archived=False)
        context['products'] = Product.objects.filter(is_active=True, is_archived=False)
        if self.request.user.is_authenticated and self.request.user.is_customer:
            customer = self.request.user.customer
            order = Order.objects.filter(customer=customer, is_active=True, completed=False).first()
        else:
            order = {}
        context['order'] = order
        return context


class Salonists(ListView):
    model = Salonist
    template_name = "home/salonists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.object_list.filter(is_active=True, is_archived=False)
        if self.request.user.is_authenticated and self.request.user.is_customer:
            customer = self.request.user.customer
            order = Order.objects.filter(customer=customer, is_active=True, completed=False).first()
        else:
            order = {}
        context['order'] = order
        return context


def privacy_policy(request):
    if request.user.is_authenticated and request.user.is_customer:
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, is_active=True, completed=False).first()
    else:
        order = {}
    return render(request, "home/privacy-policy.html", {'order': order})


def about_us(request):
    if request.user.is_authenticated and request.user.is_customer:
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, is_active=True, completed=False).first()
    else:
        order = {}
    return render(request, "home/about-us.html", {'order': order})


def search(request):
    q = request.GET.get('search')
    services = Service.objects.filter(
        Q(name__icontains=q) | Q(description__icontains=q))
    services_count = Service.objects.filter(
        Q(name__icontains=q) | Q(description__icontains=q)).count()
    products = Product.objects.filter(
        Q(name__icontains=q) | Q(description__icontains=q))
    products_count = Product.objects.filter(
        Q(name__icontains=q) | Q(description__icontains=q)).count()
    salonists = Salonist.objects.filter(
        Q(first_name__icontains=q) | Q(last_name__icontains=q) & Q(is_active=True))
    salonists_count = Salonist.objects.filter(
        Q(first_name__icontains=q) | Q(last_name__icontains=q) & Q(is_active=True)).count()
    count = services_count + products_count + salonists_count
    context = {
        'services': services, 'products': products, 'search': q, 'salonists': salonists, 'count': count,
    }
    return render(request, 'home/search.html', context)


def term_condition(request):
    return render(request, "home/term-condition.html")
