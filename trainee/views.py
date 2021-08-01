from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import NoReverseMatch, reverse
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import ListView, CreateView

from trainee.forms import TraineeSignUpForm, TraineeFeedbackForm, TraineeProfileForm, TraineeForm, \
    TrainingApplicationForm, TrainingPaymentForm
from trainee.models import Trainee, TraineeFeedback, TrainingApplication, TrainingPayment
from salonist.tokens import account_activation_token
from service.forms import BookingPaymentForm
from service.models import Service, Booking, Apprenticeship, BookingPayment, Appointment
from store.forms import OrderPaymentForm
from store.models import Order, Product, OrderItem, OrderPayment, Wishlist
from user.decorators import trainee_required
from user.models import CustomUser
from utils.utils import generate_key


# from mpesa_api.core.mpesa import Mpesa


class Home(ListView):
    model = TrainingApplication
    template_name = "trainee/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trainee = self.request.user.trainee
        context['object_list'] = self.object_list.filter(trainee=trainee)
        context['paid_trainee_count'] = context['object_list'].filter(is_paid=True).count()
        context['not_paid_trainee_count'] = context['object_list'].filter(is_paid=False).count()
        context['pending_trainee_count'] = context['object_list'].filter(is_approved=False).count()
        context['approved_trainee_count'] = context['object_list'].filter(is_approved=True).count()
        return context


def login(request):
    if request.method == "POST":
        remember = request.POST.get('remember')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if not remember == "remember-me":
            request.session.set_expiry(0)
        if user is not None:
            if not user.is_active and user.is_trainee and not user.is_archived:
                if user.is_verified:
                    messages.info(request,
                                  "your email is verified, but your account is "
                                  "inactive. Check your mail for notification.")
                else:
                    messages.info(request,
                                  "your email is not verified, verify your email.")
            elif user.is_active and user.is_trainee and not user.is_archived:
                if user.is_verified:
                    auth_login(request, user)
                    user = request.user.get_full_name
                    messages.success(request, f"Hi {user}, welcome to Ashley's Salon.")
                    try:
                        if 'add_to_cart' in request.GET.get('next', 'trainee:index'):
                            return redirect('trainee:index')
                        else:
                            return redirect(request.GET.get('next', 'trainee:index'))
                    except (NoReverseMatch, ImproperlyConfigured):
                        return redirect("trainee:index")
                else:
                    messages.info(request,
                                  "you've registered, but your email is not verified, verify your email and try again.")
            else:
                messages.info(request, f"Hi {user.get_full_name}, "
                                       f"you can't login here, this login page is for Trainees only.")
                logout(request)
                try:
                    return redirect(request.GET.get('next', ''))
                except (NoReverseMatch, ImproperlyConfigured):
                    return redirect("trainee:login")
        else:
            messages.info(request, "your email or password is incorrect. Please check.")
            try:
                return redirect(request.GET.get('next', ''))
            except (NoReverseMatch, ImproperlyConfigured):
                return redirect("trainee:login")
    return render(request, 'trainee/accounts/login.html')


class TraineeSignUpView(CreateView):
    form_class = TraineeSignUpForm
    template_name = "trainee/accounts/register.html"

    def get_form_kwargs(self):
        kwargs = super(TraineeSignUpView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = {
            'form': form,
        }
        messages.info(self.request, "Please correct errors below")
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
        # user.is_active = True
        user.is_verified = True
        user.save()
        # current_site = get_current_site(self.request)
        # to_email = form.cleaned_data.get('email')
        # subject = f"Ashley's Salon Trainee Email Verification."
        # msg_plain = render_to_string('trainee/emails/email.txt', {'user_name': user.get_full_name, })
        # msg_html = render_to_string('trainee/emails/account_activation_email.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': account_activation_token.make_token(user),
        # })
        # send_mail(subject, msg_plain, "Ashley's Salon", [to_email], html_message=msg_html)
        messages.success(self.request,
                         f"Hi {name} {last}, your account has been created successfully wait for approval.")
        return redirect("trainee:login")


class VerifyEmail(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Trainee.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None
        data = {}
        if user is not None and account_activation_token.check_token(user, token):
            if user.is_verified:
                messages.info(request, "you've already confirmed your email.")
                data['message'] = "you've already confirmed your email."
            elif not user.is_verified:
                user.is_verified = True
                user.save()
                data['message'] = "You've successfully verified your email. use your email to login"
        else:
            data['message'] = 'The confirmation link was invalid, possibly because it has already been used.'
        return JsonResponse(data)


def profile(request):
    data = {}
    p_form = TraineeProfileForm(instance=request.user.trainee.traineeprofile)
    form = TraineeForm(instance=request.user.trainee)
    if request.method == "POST":
        p_form = TraineeProfileForm(request.POST, request.FILES, instance=request.user.trainee.traineeprofile)
        form = TraineeForm(request.POST, instance=request.user.trainee)
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            messages.success(request, "Your Profile has been updated!")
    data['form'] = form
    data['p_form'] = p_form
    return render(request, 'trainee/forms/profile.html', data)


def faq(request):  # Not Done
    return render(request, 'trainee/faq.html')


def change_password(request):
    context = {}
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
    context['form'] = form
    return render(request, 'trainee/forms/change-password.html', context)


def feedback(request):
    data = {}
    form = TraineeFeedbackForm
    if request.method == "POST":
        form = TraineeFeedbackForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user.trainee
            admin = CustomUser.objects.filter(is_staff=True, is_superuser=True, is_active=True).first()
            instance.admin = admin
            if TraineeFeedback.objects.filter(subject=instance.subject, message=instance.message,
                                              user=instance.user, admin=admin).exists():
                messages.info(request, "You've already sent this feedback, thank you.")
            elif TraineeFeedback.objects.filter(subject=instance.subject, user=instance.user,
                                                admin=admin).exists():
                messages.info(request, "You've already sent this feedback, thank you.")
            elif TraineeFeedback.objects.filter(message=instance.message, user=instance.user,
                                                admin=admin).exists():
                messages.info(request, "You've already sent this feedback, thank you.")
                data['info'] = "You've already sent this feedback, thank you."
            else:
                instance.save()
                messages.success(request, "Feedback has been sent. Thank you")
    data['form'] = form
    return render(request, 'trainee/forms/feedback.html', data)


def apply_training(request):
    data = {}
    form = TrainingApplicationForm
    if request.method == "POST":
        form = TrainingApplicationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.code = generate_key(8, 8)
            instance.trainee = request.user.trainee
            if TrainingApplication.objects.filter(training=instance.training, trainee=instance.trainee,
                                                  is_done=False).exists():
                messages.info(request, f"You have an ongoing training for {instance.training}.")
            else:
                instance.save()
                messages.success(request, f"You've applied successfully for{instance.training}")
    data['form'] = form
    return render(request, 'trainee/forms/apply-training.html', data)


def training_payment(request):
    data = {}
    form = TrainingPaymentForm
    if request.method == "POST":
        form = TrainingPaymentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            mpesa = instance.mpesa
            instance.trainee = request.user.trainee
            if len(mpesa) == 10:
                if instance.amount == instance.training.training.price:
                    instance.code = generate_key(8, 8)
                    if TrainingPayment.objects.filter(training=instance.training, trainee=instance.trainee).exists():
                        messages.info(request, f"you've already paid")
                    else:
                        instance.save()
                        messages.success(request, f"Payment has been done successfully")
                else:
                    messages.info(request,
                                  f"amount sent is {instance.amount} but amount required is {instance.training.training.price}")
            else:
                messages.info(request, f"Enter valid mpesa code")
    data['form'] = form
    return render(request, 'trainee/forms/payment-form.html', data)


class PendingTrainingListView(ListView):
    model = TrainingApplication
    template_name = "trainee/tables/pending-training-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trainee = self.request.user.trainee
        context['object_list'] = self.object_list.filter(trainee=trainee, is_approved=False)
        return context


class TrainingListView(ListView):
    model = TrainingApplication
    template_name = "trainee/tables/training-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trainee = self.request.user.trainee
        context['object_list'] = self.object_list.filter(trainee=trainee, is_approved=True)
        return context


class PendingTrainingPaymentListView(ListView):
    model = TrainingPayment
    template_name = "trainee/tables/pending-payment-list.html"

    def get_context_data(self, **kwargs):
        context = super(PendingTrainingPaymentListView, self).get_context_data(**kwargs)
        trainee = self.request.user.trainee
        context['object_list'] = self.object_list.filter(trainee=trainee, is_confirmed=False)
        return context


class TrainingPaymentListView(ListView):
    model = TrainingPayment
    template_name = "trainee/tables/payment-list.html"

    def get_context_data(self, **kwargs):
        context = super(TrainingPaymentListView, self).get_context_data(**kwargs)
        trainee = self.request.user.trainee
        context['object_list'] = self.object_list.filter(trainee=trainee, is_confirmed=True)
        return context
