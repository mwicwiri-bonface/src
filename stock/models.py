from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import CustomUser, Profile, Feedback


class Stock(CustomUser):
    pass

    class Meta:
        verbose_name = 'Stock Manager'
        verbose_name_plural = ' Stock Managers'


class StockProfile(Profile):
    user = models.OneToOneField(Stock, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ' Stock Manager Profile'
        verbose_name_plural = ' Stock Manager Profiles'


class StockFeedback(Feedback):
    user = models.ForeignKey(Stock, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ' Stock Manager'
        verbose_name_plural = ' Stock Manager Feedback'


@receiver(post_save, sender=Stock)
def stock_profile(sender, instance, created, **kwargs):
    if created:
        StockProfile.objects.create(user=instance)
        instance.stockprofile.save()

