from django.forms import ModelForm

from service.models import Service, SalonistService, Booking, BookingPayment, Appointment, Apprenticeship, \
    ApprenticeshipApplication


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'image']


class SalonistServiceForm(ModelForm):
    class Meta:
        model = SalonistService
        fields = ['service', 'salonist']


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['service']


class BookingPaymentForm(ModelForm):
    class Meta:
        model = BookingPayment
        fields = ['mpesa', 'phone', 'amount']


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['stop_date', 'date']


class ApprenticeshipForm(ModelForm):
    class Meta:
        model = Apprenticeship
        fields = ['date', 'salonist']


class ApprenticeshipApplicationForm(ModelForm):
    class Meta:
        model = ApprenticeshipApplication
        fields = ['program']
