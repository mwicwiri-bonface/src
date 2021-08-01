from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import CustomUser, Profile, Feedback


class Finance(CustomUser):
    pass

    class Meta:
        verbose_name = 'Finance'
        verbose_name_plural = 'Finances'


class FinanceProfile(Profile):
    user = models.OneToOneField(Finance, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Finance Profile'
        verbose_name_plural = 'Finances Profile'


class FinanceFeedback(Feedback):
    user = models.ForeignKey(Finance, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Finance Feedback'
        verbose_name_plural = 'Finance Feedback'


@receiver(post_save, sender=Finance)
def finance_profile(sender, instance, created, **kwargs):
    if created:
        FinanceProfile.objects.create(user=instance)
        instance.financeprofile.save()
