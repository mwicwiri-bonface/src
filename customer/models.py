from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from shipment.models import ShipmentLocations
from user.models import CustomUser, Profile, Feedback


class Customer(CustomUser):
    pass

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class CustomerProfile(Profile):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE)
    location = models.ForeignKey(ShipmentLocations, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Customer Profile'
        verbose_name_plural = 'Customers Profile'


class CustomerFeedback(Feedback):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Customer Feedback'
        verbose_name_plural = 'Customers Feedback'


@receiver(post_save, sender=Customer)
def customer_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(user=instance)
        instance.customerprofile.save()

