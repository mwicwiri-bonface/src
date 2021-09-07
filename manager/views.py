from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.db.models import Sum, Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import NoReverseMatch
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import ListView, CreateView
from weasyprint import HTML

from customer.models import Customer
from manager.forms import ManagerProfileForm, ManagerForm, ManagerSignUpForm, ManagerFeedbackForm
from manager.models import Manager, ManagerFeedback
from manager.tokens import account_activation_token
from salonist.forms import SalonistForm, SalonistSignUpForm
from salonist.models import Salonist
from service.forms import ServiceForm, ApprenticeshipForm, SalonistServiceForm
from service.models import Appointment, BookingPayment, Service, Apprenticeship, SalonistService
from store.forms import ProductForm
from store.models import Product
from trainee.forms import TrainingForm
from trainee.models import Training, TrainingApplication
from user.decorators import manager_required
from user.models import CustomUser


def error_404(request, exception):
    return render(request, 'errors/error-404.html')


def error_403(request, exception):
    return render(request, 'errors/error-403.html')


def error_500(request):
    return render(request, 'errors/error-500.html')


def error_503(request, exception):
    return render(request, 'errors/error-503.html')


def login(request):
    if request.method == "POST":
        remember = request.POST.get('remember')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if not remember == "remember-me":
            request.session.set_expiry(0)
        if user is not None:
            if not user.is_active and user.is_manager and not user.is_archived:
                if user.is_verified:
                    messages.info(request,
                                  "your email is verified, but your account is "
                                  "inactive. Check your mail for notification.")
                else:
                    messages.info(request,
                                  "your email is not verified, verify your email.")
            elif user.is_active and user.is_manager and not user.is_archived:
                if user.is_verified:
                    auth_login(request, user)
                    user = request.user.get_full_name
                    messages.success(request, f"Hi {user}, welcome to Manager's Portal.")
                    try:
                        return redirect(request.GET.get('next', 'manager:index'))
                    except (NoReverseMatch, ImproperlyConfigured):
                        return redirect("manager:index")
                else:
                    messages.info(request,
                                  "you've registered, but your email is not verified, verify your email and try again.")
            else:
                messages.info(request, f"Hi {user.get_full_name}, "
                                       f"you can't login here, this login page is for Managers only.")
                logout(request)
                try:
                    return redirect(request.GET.get('next', ''))
                except (NoReverseMatch, ImproperlyConfigured):
                    return redirect("manager:login")
        else:
            messages.info(request, "your email or password is incorrect. Please check.")
            try:
                return redirect(request.GET.get('next', ''))
            except (NoReverseMatch, ImproperlyConfigured):
                return redirect("manager:login")
    return render(request, 'manager/accounts/login.html')


class ManagerSignUpView(CreateView):
    form_class = ManagerSignUpForm
    template_name = "manager/accounts/register.html"

    def get_form_kwargs(self):
        kwargs = super(ManagerSignUpView, self).get_form_kwargs()
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
        user.is_verified = True
        user.save()
        # current_site = get_current_site(self.request)
        # to_email = form.cleaned_data.get('email')
        # subject = f"Ashley's hair and beauty  Email Verification."
        # msg_plain = render_to_string('manager/emails/email.txt', {'user_name': user.get_full_name, })
        # msg_html = render_to_string('manager/emails/account_activation_email.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': account_activation_token.make_token(user),
        # })
        # send_mail(subject, msg_plain, "Ashley's hair and beauty salon", [to_email], html_message=msg_html)
        messages.success(self.request, f"Hi {name} {last}, your account has been "
                                       f"created successfully wait for approval, to login.")
        data = {
            'status': True,
            'redirect': '/manager/login'
        }
        return JsonResponse(data)


class VerifyEmail(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Manager.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            if user.is_verified:
                messages.info(request, "you've already confirmed your email.")
            elif not user.is_verified:
                user.is_verified = True
                user.save()
                messages.info(request, "You've successfully verified your email. use your email to login")
            return redirect('manager:login')
        else:
            data = {
                'message': 'The confirmation link was invalid, possibly because it has already been used.'
            }
            return JsonResponse(data)


class Home(ListView):
    model = Manager
    template_name = "manager/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['salonists_count'] = Salonist.objects.filter(is_active=True).count()
        context['salonists_per'] = int((context['salonists_count'] / Salonist.objects.all().count()) * 100)
        context['salonists'] = Salonist.objects.filter(is_active=True)
        context['customers'] = Customer.objects.all()
        context['customers_count'] = context['customers'].filter(is_active=True).count()
        context['customers_per'] = int((context['customers_count'] / context['customers'].count()) * 100)
        context['appointments'] = Appointment.objects.all()
        context['appointment_count'] = context['appointments'].filter(stop_date__gt=timezone.now()).count()
        context['appointment_per'] = int((context['appointment_count'] / context['appointments'].count()) * 100)
        context['total_amount'] = BookingPayment.objects.all().aggregate(Sum('amount')).get('amount__sum', 0.00)
        return context


class CustomersListView(ListView):
    model = Customer
    template_name = "manager/tables/customers-list.html"


class SalonistsListView(ListView):
    model = Salonist
    template_name = "manager/tables/salonists-list.html"


class ProductsListView(ListView):
    model = Product
    template_name = "manager/tables/products-list.html"


class ServicesListView(ListView):
    model = Service
    template_name = "manager/tables/services-list.html"


class ApprenticeshipListView(ListView):
    model = Apprenticeship
    template_name = "manager/tables/apprenticeship-list.html"


class SalonistServiceListView(ListView):
    model = SalonistService
    template_name = "manager/tables/salonists-service-list.html"


class ServiceCreateView(CreateView):
    form_class = ServiceForm
    template_name = "manager/forms/service-create.html"

    def get_form_kwargs(self):
        kwargs = super(ServiceCreateView, self).get_form_kwargs()
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
        if Service.objects.filter(name=instance.name).exists():
            messages.info(self.request, f"{instance.name}, has already been added.")
        else:
            instance.save()
            messages.success(self.request, f"{instance.name} has been added successfully")
        return redirect('manager:create_service')


class ProductCreateView(CreateView):
    form_class = ProductForm
    template_name = "manager/forms/product-create.html"

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
        return redirect('manager:create_product')


class SalonistCreateView(CreateView):
    form_class = SalonistSignUpForm
    template_name = "manager/forms/salonist-create.html"

    def get_form_kwargs(self):
        kwargs = super(SalonistCreateView, self).get_form_kwargs()
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
        instance.is_approved = True
        instance.is_verified = True
        instance.save()
        messages.success(self.request, f"{instance.name} has been added successfully")
        return redirect('manager:create_salonist')


class ApprenticeshipCreateView(CreateView):
    form_class = ApprenticeshipForm
    template_name = "manager/forms/apprenticeship-create.html"

    def get_form_kwargs(self):
        kwargs = super(ApprenticeshipCreateView, self).get_form_kwargs()
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
        if Apprenticeship.objects.filter(salonist=instance.salonist, is_active=instance.is_active,
                                         is_archived=instance.is_archived).exists():
            messages.info(self.request, f"{instance.salonist.get_full_name}, has active apprenticeship.")
        else:
            instance.save()
            messages.success(self.request, f"Apprenticeship has been added successfully")
        return redirect('manager:create_apprenticeship')


class SalonistServiceCreateView(CreateView):
    form_class = SalonistServiceForm
    template_name = "manager/forms/salonist-service-create.html"

    def get_form_kwargs(self):
        kwargs = super(SalonistServiceCreateView, self).get_form_kwargs()
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
        if SalonistService.objects.filter(salonist=instance.salonist, service=instance.service,
                                          is_active=instance.is_active,
                                          is_archived=instance.is_archived).exists():
            messages.info(self.request, f"{instance.service.name} has already been assigned to "
                                        f"{instance.salonist.get_full_name}.")
        else:
            instance.save()
            messages.success(self.request, f"{instance.service.name} has been assigned to "
                                           f"{instance.salonist.get_full_name}.")
        return redirect('manager:create_salonist_service')


@manager_required
def profile_main(request):
    p_form = ManagerProfileForm(instance=request.user.manager.managerprofile)
    form = ManagerForm(instance=request.user.manager)
    if request.method == "POST":
        p_form = ManagerProfileForm(request.POST, request.FILES, instance=request.user.manager.managerprofile)
        form = ManagerForm(request.POST, instance=request.user.manager)
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            messages.success(request, "Your Profile has been updated!")
    context = {
        'p_form': p_form,
        'form': form,
    }
    return render(request, 'manager/forms/profile.html', context)


@manager_required
def faq(request):  # Not Done
    context = {}
    return render(request, 'manager/faq.html', context)


@manager_required
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
    return render(request, 'manager/forms/change-password.html', {'form': form})


@manager_required
def feedback(request):
    form = ManagerFeedbackForm
    if request.method == "POST":
        form = ManagerFeedbackForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user.manager
            admin = CustomUser.objects.filter(is_staff=True, is_superuser=True, is_active=True).first()
            instance.admin = admin
            if ManagerFeedback.objects.filter(subject=instance.subject, message=instance.message, user=instance.user,
                                              admin=admin).exists():
                messages.info(request, "You've already sent this feedback, thank you.")
            elif ManagerFeedback.objects.filter(subject=instance.subject, user=instance.user, admin=admin).exists():
                messages.info(request, "You've already sent this feedback, thank you.")
            elif ManagerFeedback.objects.filter(message=instance.message, user=instance.user, admin=admin).exists():
                messages.info(request, "You've already sent this feedback, thank you.")
            else:
                instance.save()
                messages.success(request, "Feedback has been sent. Thank you")
    return render(request, 'manager/forms/feedback.html', {'form': form})


@manager_required
def search(request):
    q = request.GET.get('search')
    context = {}
    products = Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    services = Service.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    context['products'] = products
    context['services'] = services
    context['q'] = q
    return render(request, 'manager/search.html', context)


class TrainingCreateView(CreateView):
    form_class = TrainingForm
    template_name = "manager/forms/training-create.html"

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
        return redirect('manager:add_training')


class TrainingListView(ListView):
    model = Training
    template_name = "manager/tables/training-list.html"

    def get_context_data(self, **kwargs):
        context = super(TrainingListView, self).get_context_data(**kwargs)
        context['object_list'] = self.object_list.all()
        return context


class PendingTrainingListView(ListView):
    model = Training
    template_name = "manager/tables/pending-training-list.html"

    def get_context_data(self, **kwargs):
        context = super(PendingTrainingListView, self).get_context_data(**kwargs)
        context['object_list'] = self.object_list.filter(is_active=False)
        return context


class ApprovedTrainingApplicationListView(ListView):
    model = TrainingApplication
    template_name = "manager/tables/approved-training-application-list.html"

    def get_context_data(self, **kwargs):
        context = super(ApprovedTrainingApplicationListView, self).get_context_data(**kwargs)
        context['object_list'] = self.object_list.filter(is_approved=True)
        return context


class PendingTrainingApplicationListView(ListView):
    model = TrainingApplication
    template_name = "manager/tables/pending-training-application-list.html"

    def get_context_data(self, **kwargs):
        context = super(PendingTrainingApplicationListView, self).get_context_data(**kwargs)
        context['object_list'] = self.object_list.filter(is_approved=False)
        return context


def confirm_training_application(request, application_id):
    data = {}
    if TrainingApplication.objects.filter(id=application_id, is_approved=False).exists():
        training_application = TrainingApplication.objects.get(id=application_id)
        training = training_application.training
        training_application.is_approved = True
        training_application.save()
        data['message'] = f"{training_application.trainee.get_full_name} :: application ::" \
                          f" {training_application.code} for Training {training.service.name} has been approved."
    else:
        data['info'] = f"Selected application does not exists."
    return JsonResponse(data)


def approved_training_application_pdf(request):
    """Generate pdf."""
    # Model data
    data = {'object_list': TrainingApplication.objects.filter(is_approved=True)}
    # Rendered
    html_string = render_to_string('manager/receipts/approved_training_application.html', data)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = f"inline; filename=approved-training-applications.pdf "
    return response


def pending_training_application_pdf(request):
    """Generate pdf."""
    # Model data
    data = {'object_list': TrainingApplication.objects.filter(is_approved=False)}
    # Rendered
    html_string = render_to_string('manager/receipts/pending_training_application.html', data)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = f"inline; filename=pending-training-applications.pdf "
    return response


def pending_training_pdf(request):
    """Generate pdf."""
    # Model data
    data = {'object_list': Training.objects.filter(is_active=False)}
    # Rendered
    html_string = render_to_string('manager/receipts/pending_training.html', data)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = f"inline; filename=pending-training.pdf "
    return response


def training_pdf(request):
    """Generate pdf."""
    # Model data
    data = {'object_list': Training.objects.all()}
    # Rendered
    html_string = render_to_string('manager/receipts/training.html', data)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = f"inline; filename=training.pdf "
    return response


def salonists_pdf(request):
    """Generate pdf."""
    # Model data
    data = {'object_list': Salonist.objects.all()}
    # Rendered
    html_string = render_to_string('manager/receipts/salonists.html', data)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = f"inline; filename=salonists.pdf "
    return response


def products_pdf(request):
    """Generate pdf."""
    # Model data
    data = {'object_list': Product.objects.all()}
    # Rendered
    html_string = render_to_string('manager/receipts/products.html', data)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = f"inline; filename=products.pdf "
    return response

