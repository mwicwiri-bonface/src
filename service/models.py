from django.db import models
from django.utils.translation import gettext_lazy as _
from salonist.models import Salonist, Service
from customer.models import Customer
from phonenumber_field.modelfields import PhoneNumberField

from finance.models import Finance
from manager.models import Manager


class SalonistService(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True)
    salonist = models.ForeignKey(Salonist, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    is_active = models.BooleanField(_('Active'), default=False,
                                    help_text=_('Activated, means Service will be published'))
    is_archived = models.BooleanField(_('Archive'), default=False,
                                      help_text=_('Archived, means Service will be Unpublished'))
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)


class Booking(models.Model):
    transaction_id = models.CharField(max_length=250)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(_('Appointment'), default=False, help_text=_('Means Appointment has been booked'))
    is_paid = models.BooleanField(_('Paid'), default=False, help_text=_('Means Customer has paid'))
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)

    def __str__(self):
        return f"Booking {self.transaction_id} for {self.service.name}"


class BookingPayment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    mpesa = models.CharField(max_length=10, help_text="Mpesa Code")
    phone = PhoneNumberField(blank=True, null=True)
    manager = models.ForeignKey(Finance, on_delete=models.CASCADE, null=True)
    amount = models.FloatField(default=0.0)
    confirmed = models.BooleanField(default=False, help_text="Means manager has confirmed payment")
    completed = models.BooleanField(default=False, help_text="Means customer completed payment")
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)


class Appointment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    salonist = models.ForeignKey(Salonist, on_delete=models.CASCADE)
    date = models.DateTimeField(help_text="Appointment Start Date Time")
    stop_date = models.DateTimeField(help_text="Appointment Stop Date Time")
    completed = models.BooleanField(default=False, help_text="Means customer was served")
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)


class Apprenticeship(models.Model):
    salonist = models.ForeignKey(Salonist, on_delete=models.CASCADE)
    date = models.DateTimeField(help_text="Appointment Date")
    closed = models.BooleanField(_('closed'), default=False)
    is_active = models.BooleanField(_('Active'), default=False, help_text=_('Activated, means Apprenticeship will be '
                                                                            'published'))
    is_archived = models.BooleanField(_('Archive'), default=False,
                                      help_text=_('Archived, means Apprenticeship will be Unpublished'))
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)


class ApprenticeshipApplication(models.Model):
    program = models.ForeignKey(Apprenticeship, on_delete=models.CASCADE)
    salonist = models.ForeignKey(Salonist, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    attended = models.BooleanField(help_text="Means Customer attended the program")
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
