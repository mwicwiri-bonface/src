from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import NoReverseMatch
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import ListView, CreateView

from manager.tokens import account_activation_token
from salonist.forms import SalonistForm
from salonist.forms import SalonistProfileForm, SalonistSignUpForm, SalonistFeedbackForm
from salonist.models import Salonist
from salonist.models import SalonistFeedback
from service.forms import AppointmentForm
from service.models import BookingPayment, Service, Appointment, Apprenticeship
from store.models import Product, OrderPayment
from trainee.forms import TrainingForm
from trainee.models import Training
from user.decorators import salonist_required
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
            if not user.is_active and user.is_salonist and not user.is_archived:
                if user.is_verified:
                    messages.info(request,
                                  "your email is verified, but your account is "
                                  "inactive. Check your mail for notification.")
                else:
                    messages.info(request,
                                  "your email is not verified, verify your email.")
            elif user.is_active and user.is_salonist and not user.is_archived:
                if user.is_verified:
                    auth_login(request, user)
                    user = request.user.get_full_name
                    messages.success(request, f"Hi {user}, welcome to Salonist's Portal.")
                    try:
                        return redirect(request.GET.get('next', 'salonist:index'))
                    except (NoReverseMatch, ImproperlyConfigured):
                        return redirect("salonist:index")
                else:
                    messages.info(request,
                                  "you've registered, but your email is not verified, verify your email and try again.")
            else:
                messages.info(request, f"Hi {user.get_full_name}, "
                                       f"you can't login here, this login page is for Salonists only.")
                logout(request)
                try:
                    return redirect(request.GET.get('next', ''))
                except (NoReverseMatch, ImproperlyConfigured):
                    return redirect("salonist:login")
        else:
            messages.info(request, "your email or password is incorrect. Please check.")
            try:
                return redirect(request.GET.get('next', ''))
            except (NoReverseMatch, ImproperlyConfigured):
                return redirect("salonist:login")
    return render(request, 'salonist/accounts/login.html')


class SalonistSignUpView(CreateView):
    form_class = SalonistSignUpForm
    template_name = "salonist/accounts/register.html"

    def get_form_kwargs(self):
        kwargs = super(SalonistSignUpView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.info(self.request, "Please correct errors below")
        context = {
            'form': form,
        }
        return render(self.request, self.template_name, context)

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
        # msg_plain = render_to_string('salonist/emails/email.txt', {'user_name': user.get_full_name, })
        # msg_html = render_to_string('salonist/emails/account_activation_email.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': account_activation_token.make_token(user),
        # })
        # send_mail(subject, msg_plain, "Ashley's hair and beauty salon", [to_email], html_message=msg_html)
        messages.success(self.request, f"Hi {name} {last}, your account has been "
                                       f"created successfully wait for approval, to login.")
        return redirect("salonist:login")


class VerifyEmail(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Salonist.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            if user.is_verified:
                messages.info(request, "you've already confirmed your email.")
            elif not user.is_verified:
                user.is_verified = True
                user.save()
                messages.info(request, "You've successfully verified your email. use your email to login")
            return redirect('salonist:login')
        else:
            data = {
                'message': 'The confirmation link was invalid, possibly because it has already been used.'
            }
            return JsonResponse(data)


class Home(ListView):
    model = Salonist
    template_name = "salonist/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_payment_count'] = OrderPayment.objects.filter(confirmed=False).count()
        context['order_total'] = OrderPayment.objects.all().aggregate(Sum('amount')).get('amount__sum', 0.00)
        context['booking_count'] = BookingPayment.objects.filter(confirmed=False).count()
        context['total_amount'] = BookingPayment.objects.all().aggregate(Sum('amount')).get('amount__sum', 0.00)
        return context


class AppointmentListView(ListView):
    model = Appointment
    template_name = "salonist/tables/appointment-list.html"


class ApprenticeshipListView(ListView):
    model = Apprenticeship
    template_name = "salonist/tables/apprenticeship-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.object_list.filter(closed=False).first().apprenticeshipapplication_set.all()
        return context


class ScheduleAppointmentCreateView(CreateView):
    form_class = AppointmentForm
    template_name = "salonist/forms/schedule-appointment.html"

    def get_form_kwargs(self):
        kwargs = super(ScheduleAppointmentCreateView, self).get_form_kwargs()
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
        instance.salonist = self.request.user.salonist
        instance.customer = instance.booking.customer
        if Appointment.objects.filter(salonist=instance.salonist, booking=instance.booking,
                                      customer=instance.customer).exists():
            messages.info(self.request, f"{instance.booking} has a scheduled appointment.")
        else:
            instance.save()
            messages.success(self.request, f"Appointment {instance.booking.transaction_id} has been scheduled")
        return redirect('salonist:schedule_appointment')


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


@salonist_required
def profile_main(request):
    p_form = SalonistProfileForm(instance=request.user.salonist.salonistprofile)
    form = SalonistForm(instance=request.user.salonist)
    if request.method == "POST":
        p_form = SalonistProfileForm(request.POST, request.FILES, instance=request.user.salonist.salonistprofile)
        form = SalonistForm(request.POST, instance=request.user.salonist)
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            messages.success(request, "Your Profile has been updated!")
    context = {
        'p_form': p_form,
        'form': form,
    }
    return render(request, 'salonist/forms/profile.html', context)


@salonist_required
def faq(request):  # Not Done
    context = {}
    return render(request, 'salonist/faq.html', context)


@salonist_required
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
    return render(request, 'salonist/forms/change-password.html', {'form': form})


@salonist_required
def feedback(request):
    form = SalonistFeedbackForm
    if request.method == "POST":
        form = SalonistFeedbackForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user.salonist
            admin = CustomUser.objects.filter(is_staff=True, is_superuser=True, is_active=True).first()
            instance.admin = admin
            if SalonistFeedback.objects.filter(subject=instance.subject, message=instance.message, user=instance.user,
                                               admin=admin).exists():
                messages.info(request, "You've already sent this feedback, thank you.")
            elif SalonistFeedback.objects.filter(subject=instance.subject, user=instance.user, admin=admin).exists():
                messages.info(request, "You've already sent this feedback, thank you.")
            elif SalonistFeedback.objects.filter(message=instance.message, user=instance.user, admin=admin).exists():
                messages.info(request, "You've already sent this feedback, thank you.")
            else:
                instance.save()
                messages.success(request, "Feedback has been sent. Thank you")
    return render(request, 'salonist/forms/feedback.html', {'form': form})


@salonist_required
def search(request):
    q = request.GET.get('search')
    context = {}
    products = Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    services = Service.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    context['products'] = products
    context['services'] = services
    context['q'] = q
    return render(request, 'salonist/search.html', context)


class TrainingCreateView(CreateView):
    form_class = TrainingForm
    template_name = "salonist/forms/training-create.html"

    def get_form_kwargs(self):
        kwargs = super(TrainingCreateView, self).get_form_kwargs()
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
        instance.salonist = self.request.user.salonist
        if Training.objects.filter(salonist=instance.salonist, service=instance.service,
                                   price=instance.price, is_active=False).exists():
            messages.info(self.request, f"Active {instance.service} already exists.")
        else:
            instance.save()
            messages.success(self.request, f"Training for {instance.service.name} has been added successfully.")
        return redirect('salonist:add_training')


class TrainingListView(ListView):
    model = Training
    template_name = "salonist/tables/training-list.html"

    def get_context_data(self, **kwargs):
        context = super(TrainingListView, self).get_context_data(**kwargs)
        context['object_list'] = self.object_list.filter(salonist=self.request.user.salonist)
        return context
