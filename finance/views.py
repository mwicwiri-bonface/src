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
from finance.forms import FinanceProfileForm, FinanceForm, FinanceSignUpForm, FinanceFeedbackForm
from finance.models import Finance, FinanceFeedback
from manager.tokens import account_activation_token
from salonist.forms import SalonistForm
from salonist.models import Salonist
from service.forms import ServiceForm, ApprenticeshipForm  # , SalonistServiceForm
from service.models import Appointment, BookingPayment, Service, Apprenticeship, SalonistService
from store.forms import ProductForm
from store.models import Product, OrderPayment
from trainee.models import TrainingPayment
from user.decorators import finance_required
from user.models import CustomUser


def error_404(request, exception):
    return render(request, 'finance/error/errors-404.html')


def error_403(request, exception):
    return render(request, 'finance/error/errors-403.html')


def error_500(request):
    return render(request, 'finance/error/errors-500.html')


def error_503(request, exception):
    return render(request, 'finance/errors-503.html')


def login(request):
    if request.method == "POST":
        remember = request.POST.get('remember')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if not remember == "remember-me":
            request.session.set_expiry(0)
        if user is not None:
            if not user.is_active and user.is_finance and not user.is_archived:
                if user.is_verified:
                    messages.info(request,
                                  "your email is verified, but your account is "
                                  "inactive. Check your mail for notification.")
                else:
                    messages.info(request,
                                  "your email is not verified, verify your email.")
            elif user.is_active and user.is_finance and not user.is_archived:
                if user.is_verified:
                    auth_login(request, user)
                    user = request.user.get_full_name
                    messages.success(request, f"Hi {user}, welcome to Finance's Portal.")
                    try:
                        return redirect(request.GET.get('next', 'finance:index'))
                    except (NoReverseMatch, ImproperlyConfigured):
                        return redirect("finance:index")
                else:
                    messages.info(request,
                                  "you've registered, but your email is not verified, verify your email and try again.")
            else:
                messages.info(request, f"Hi {user.get_full_name}, "
                                       f"you can't login here, this login page is for Finances only.")
                logout(request)
                try:
                    return redirect(request.GET.get('next', ''))
                except (NoReverseMatch, ImproperlyConfigured):
                    return redirect("finance:login")
        else:
            messages.info(request, "your email or password is incorrect. Please check.")
            try:
                return redirect(request.GET.get('next', ''))
            except (NoReverseMatch, ImproperlyConfigured):
                return redirect("finance:login")
    return render(request, 'finance/accounts/login.html')


class FinanceSignUpView(CreateView):
    form_class = FinanceSignUpForm
    template_name = "finance/accounts/register.html"

    def get_form_kwargs(self):
        kwargs = super(FinanceSignUpView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):



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
        user.is_verified = True
        user.save()
        # current_site = get_current_site(self.request)
        # to_email = form.cleaned_data.get('email')
        # subject = f"Ashley's hair and beauty  Email Verification."
        # msg_plain = render_to_string('finance/emails/email.txt', {'user_name': user.get_full_name, })
        # msg_html = render_to_string('finance/emails/account_activation_email.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': account_activation_token.make_token(user),
        # })
        # send_mail(subject, msg_plain, "Ashley's hair and beauty salon", [to_email], html_message=msg_html)
        messages.success(self.request, f"Hi {name} {last}, your account has been "
                                       f"created successfully wait for approval, to login.")
        return redirect("finance:login")


class VerifyEmail(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Finance.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            if user.is_verified:
                messages.info(request, "you've already confirmed your email.")
            elif not user.is_verified:
                user.is_verified = True
                user.save()
                messages.info(request, "You've successfully verified your email. use your email to login")
            return redirect('finance:login')
        else:
            data = {
                'message': 'The confirmation link was invalid, possibly because it has already been used.'
            }
            return JsonResponse(data)


class Home(ListView):
    model = Finance
    template_name = "finance/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_payment_count'] = OrderPayment.objects.filter(confirmed=False).count()
        context['order_total'] = OrderPayment.objects.all().aggregate(Sum('amount')).get('amount__sum', 0.00)
        context['booking_count'] = BookingPayment.objects.filter(confirmed=False).count()
        context['total_amount'] = BookingPayment.objects.all().aggregate(Sum('amount')).get('amount__sum', 0.00)
        return context


class BookingPaymentListView(ListView):
    model = BookingPayment
    template_name = "finance/tables/booking-payment-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.object_list.filter(confirmed=True)
        return context


class PendingBookingPaymentListView(ListView):
    model = BookingPayment
    template_name = "finance/tables/pending-booking-payment-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.object_list.filter(confirmed=False)
        return context


class OrderPaymentListView(ListView):
    model = OrderPayment
    template_name = "finance/tables/order-payment-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.object_list.filter(confirmed=True)
        return context


class PendingOrderPaymentListView(ListView):
    model = OrderPayment
    template_name = "finance/tables/pending-order-payment-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.object_list.filter(confirmed=False)
        return context


def confirm_order_payment(request, order_id):
    data = {}
    if OrderPayment.objects.filter(id=order_id).exists():
        payment = OrderPayment.objects.get(id=order_id)
        order = payment.order
        payment.confirmed = True
        payment.save()
        order.completed = True
        order.save()
        data['message'] = f"payment for order {order.transaction_id} has been confirmed."
    else:
        data['info'] = f"Selected payment does not exists."
    return JsonResponse(data)


def confirm_booking_payment(request, booking_id):
    data = {}
    if BookingPayment.objects.filter(id=booking_id).exists():
        payment = BookingPayment.objects.get(id=booking_id)
        booking = payment.booking
        payment.confirmed = True
        payment.save()
        booking.completed = True
        booking.save()
        data['message'] = f"payment for booking {booking.transaction_id} has been confirmed."
    else:
        data['info'] = f"Selected payment does not exists."
    return JsonResponse(data)


@finance_required
def profile_main(request):
    p_form = FinanceProfileForm(instance=request.user.finance.financeprofile)
    form = FinanceForm(instance=request.user.finance)
    if request.method == "POST":
        p_form = FinanceProfileForm(request.POST, request.FILES, instance=request.user.finance.financeprofile)
        form = FinanceForm(request.POST, instance=request.user.finance)
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            messages.success(request, "Your Profile has been updated!")
    context = {
        'p_form': p_form,
        'form': form,
    }
    return render(request, 'finance/forms/profile.html', context)


@finance_required
def faq(request):  # Not Done
    context = {}
    return render(request, 'finance/faq.html', context)


@finance_required
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
    return render(request, 'finance/forms/change-password.html', {'form': form})


@finance_required
def feedback(request):
    form = FinanceFeedbackForm
    if request.method == "POST":
        form = FinanceFeedbackForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user.finance
            admin = CustomUser.objects.filter(is_staff=True, is_superuser=True, is_active=True).first()
            instance.admin = admin
            if FinanceFeedback.objects.filter(subject=instance.subject, message=instance.message, user=instance.user,
                                              admin=admin).exists():
                messages.info(request, "You've already sent this feedback, thank you.")
            elif FinanceFeedback.objects.filter(subject=instance.subject, user=instance.user, admin=admin).exists():
                messages.info(request, "You've already sent this feedback, thank you.")
            elif FinanceFeedback.objects.filter(message=instance.message, user=instance.user, admin=admin).exists():
                messages.info(request, "You've already sent this feedback, thank you.")
            else:
                instance.save()
                messages.success(request, "Feedback has been sent. Thank you")
    return render(request, 'finance/forms/feedback.html', {'form': form})


@finance_required
def search(request):
    q = request.GET.get('search')
    context = {}
    products = Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    services = Service.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    context['products'] = products
    context['services'] = services
    context['q'] = q
    return render(request, 'finance/search.html', context)


class PendingTrainingPaymentListView(ListView):
    model = TrainingPayment
    template_name = "finance/tables/pending-payment-list.html"

    def get_context_data(self, **kwargs):
        context = super(PendingTrainingPaymentListView, self).get_context_data(**kwargs)
        context['object_list'] = self.object_list.filter( is_confirmed=False)
        return context


class TrainingPaymentListView(ListView):
    model = TrainingPayment
    template_name = "finance/tables/payment-list.html"

    def get_context_data(self, **kwargs):
        context = super(TrainingPaymentListView, self).get_context_data(**kwargs)
        context['object_list'] = self.object_list.filter(is_confirmed=True)
        return context


def confirm_training_payment(request, slug):
    data = {}
    if TrainingPayment.objects.filter(id=slug).exists():
        instance = TrainingPayment.objects.get(id=slug)
        instance.finance = request.user.finance
        instance.is_confirmed = True
        instance.save()
        instance = instance.training
        instance.is_paid = True
        instance.is_approved = True
        instance.save()
        data['message'] = f"payment {instance.code} has been confirmed successfully."
    else:
        data['info'] = f"Selected payment does not exists."
    return JsonResponse(data)
