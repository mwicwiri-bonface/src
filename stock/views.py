from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import NoReverseMatch
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import ListView, CreateView

from customer.models import Customer
from salonist.models import Salonist
from service.models import Appointment, BookingPayment, Service
from stock.forms import StockProfileForm, StockForm, StockSignUpForm, StockFeedbackForm
from stock.models import Stock, StockFeedback
from store.forms import ProductForm
from store.models import Product
from user.decorators import stock_required
from user.models import CustomUser


def login(request):
    if request.method == "POST":
        remember = request.POST.get('remember')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if not remember == "remember-me":
            request.session.set_expiry(0)
        if user is not None:
            if not user.is_active and user.is_stock and not user.is_archived:
                if user.is_verified:
                    messages.info(request,
                                  "your email is verified, but your account is "
                                  "inactive. Check your mail for notification.")
                else:
                    messages.info(request,
                                  "your email is not verified, verify your email.")
            elif user.is_active and user.is_stock and not user.is_archived:
                if user.is_verified:
                    auth_login(request, user)
                    user = request.user.get_full_name
                    messages.success(request, f"Hi {user}, welcome to Stock's Portal.")
                    try:
                        return redirect(request.GET.get('next', 'stock:index'))
                    except (NoReverseMatch, ImproperlyConfigured):
                        return redirect("stock:index")
                else:
                    messages.info(request,
                                  "you've registered, but your email is not verified, verify your email and try again.")
            else:
                messages.info(request, f"Hi {user.get_full_name}, "
                                       f"you can't login here, this login page is for Stocks only.")
                logout(request)
                try:
                    return redirect(request.GET.get('next', ''))
                except (NoReverseMatch, ImproperlyConfigured):
                    return redirect("stock:login")
        else:
            messages.info(request, "your email or password is incorrect. Please check.")
            try:
                return redirect(request.GET.get('next', ''))
            except (NoReverseMatch, ImproperlyConfigured):
                return redirect("stock:login")
    return render(request, 'stock/accounts/login.html')


class StockSignUpView(CreateView):
    form_class = StockSignUpForm
    template_name = "stock/accounts/register.html"

    def get_form_kwargs(self):
        kwargs = super(StockSignUpView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = {
            'info': "Please correct errors below",
            'form': form.errors,
        }
        return JsonResponse(context, status=200)

    def form_valid(self, form):
        name = form.instance.first_name
        last = form.instance.last_name
        username = form.instance.email
        username = username.lower()
        form.instance.email = username
        if '@gmail.com' in username:
            username = username.replace('@gmail.com', '')
        elif '@yahoo.com' in username:
            username = username.replace('@yahoo.com', '')
        elif '@hotmail.com' in username:
            username = username.replace('@hotmail.com', '')
        elif '@live.com' in username:
            username = username.replace('@live.com', '')
        elif '@msn.com' in username:
            username = username.replace('@msn.com', '')
        elif '@passport.com' in username:
            username = username.replace('@passport.com', '')
        elif '@outlook.com' in username:
            username = username.replace('@outlook.com', '')
        form.instance.username = username
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        messages.success(self.request, f"Hi {name} {last}, your account has been "
                                       f"created successfully verify your email, to login.")
        data = {
            'status': True,
            'redirect': '/stock/login'
        }
        return JsonResponse(data)


class Home(ListView):
    model = Stock
    template_name = "stock/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['salonists_count'] = Salonist.objects.filter(is_active=True).count()
        context['salonists'] = Salonist.objects.filter(is_active=True)
        context['customers_count'] = Customer.objects.filter(is_active=True).count()
        context['customers'] = Customer.objects.filter(is_active=True)
        context['appointment_count'] = Appointment.objects.all().count()
        context['appointments'] = Appointment.objects.all()
        context['total_amount'] = BookingPayment.objects.all().aggregate(Sum('amount')).get('amount__sum', 0.00)
        # amounts = list(BookingPayment.objects.all().values_list('amount', Flat=True))
        return context


class ProductsListView(ListView):
    model = Product
    template_name = "stock/tables/products-list.html"


class ProductCreateView(CreateView):
    form_class = ProductForm
    template_name = "stock/forms/product-create.html"

    def get_form_kwargs(self):
        kwargs = super(ProductCreateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = {
            'info': "Please correct errors below",
            'form': form,
        }
        return render(self.request, self.template_name, context)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.is_active = True
        instance.save()
        messages.success(self.request, f"{instance.name} has been added successfully")
        return redirect('stock:create_product')


@stock_required
def profile_main(request):
    p_form = StockProfileForm(instance=request.user.stock.stockprofile)
    form = StockForm(instance=request.user.stock)
    if request.method == "POST":
        p_form = StockProfileForm(request.POST, request.FILES, instance=request.user.stock.stockprofile)
        form = StockForm(request.POST, instance=request.user.stock)
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            messages.success(request, "Your Profile has been updated!")
    context = {
        'p_form': p_form,
        'form': form,
    }
    return render(request, 'stock/forms/profile.html', context)


@stock_required
def faq(request):  # Not Done
    context = {}
    return render(request, 'stock/faq.html', context)


@stock_required
def password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.info(request, 'Please correct the errors below.')
    return render(request, 'stock/forms/change-password.html', {'form': form})


@stock_required
def feedback(request):
    form = StockFeedbackForm
    if request.method == "POST":
        form = StockFeedbackForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user.stock
            admin = CustomUser.objects.filter(is_staff=True, is_superuser=True, is_active=True).first()
            instance.admin = admin
            if StockFeedback.objects.filter(subject=instance.subject, message=instance.message, user=instance.user,
                                            admin=admin).exists():
                messages.info(request, "You've already sent this feedback, thank you.")
            elif StockFeedback.objects.filter(subject=instance.subject, user=instance.user, admin=admin).exists():
                messages.info(request, "You've already sent this feedback, thank you.")
            elif StockFeedback.objects.filter(message=instance.message, user=instance.user, admin=admin).exists():
                messages.info(request, "You've already sent this feedback, thank you.")
            else:
                instance.save()
                messages.success(request, "Feedback has been sent. Thank you")
    return render(request, 'stock/forms/feedback.html', {'form': form})


@stock_required
def search(request):
    q = request.GET.get('search')
    context = {}
    products = Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    services = Service.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    context['products'] = products
    context['services'] = services
    context['q'] = q
    return render(request, 'stock/search.html', context)
