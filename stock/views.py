from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.db.models import Sum, Q
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
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
from store.forms import ProductForm, GalleryForm
from store.models import Product, Gallery
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
                messages.info(request, "You've registered but your account is pending.")
            elif user.is_active and user.is_stock and not user.is_archived:
                auth_login(request, user)
                user = request.user.get_full_name
                messages.success(request, f"Hi {user}, welcome to Stock's Portal.")
                try:
                    return redirect(request.GET.get('next', 'stock:index'))
                except (NoReverseMatch, ImproperlyConfigured):
                    return redirect("stock:index")
            else:
                messages.info(request, f"Hi {user.get_full_name}, "
                                       f"you can't login here, this login page is for Stock managers only.")
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
        # user.is_active = True
        user.is_verified = True
        user.save()
        messages.success(self.request, f"Hi {name} {last}, your account has been "
                                       f"created successfully  wait for approval, to login.")
        data = {
            'status': True,
            'redirect': '/stock/login'
        }
        return JsonResponse(data)


class Home(ListView):
    model = Product
    template_name = "stock/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.object_list
        context['active_products'] = context['products'].filter(is_active=True)
        context['pending_products'] = context['products'].filter(is_active=False)
        context['stock_out_products'] = context['products'].filter(quantity__lte=0)
        context['active_products_count'] = context['products'].filter(is_active=True).count()
        context['pending_products_count'] = context['products'].filter(is_active=False).count()
        context['stock_out_products_count'] = context['products'].filter(quantity__lte=0).count()
        context['active_products_progress'] = int((context['active_products_count'] / context['products'].count())
                                                  * 100)
        context['pending_products_progress'] = int((context['pending_products_count'] / context['products'].count())
                                                   * 100)
        context['stock_out_products_progress'] = int((context['stock_out_products_count'] / context['products'].count())
                                                     * 100)
        context['products'] = self.object_list.filter(quantity__gte=1)
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


def add_product_gallery(request, slug):
    context = {}
    product = get_object_or_404(Product, slug=slug)
    product_formset = inlineformset_factory(Product, Gallery, form=GalleryForm, extra=1, max_num=6)
    formset = product_formset(instance=product)
    if request.method == 'POST':
        formset = product_formset(request.POST, request.FILES, instance=product)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.product = product
                    instance.save()
                    messages.success(request, f"{product.name} gallery has been saved successfully.")
    context['object'] = product
    context['formset'] = formset
    return render(request, 'stock/forms/create-gallery.html', context)
