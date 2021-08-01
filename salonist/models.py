from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import CustomUser, Profile, Feedback
from django.utils.translation import gettext_lazy as _


class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="service/%y/%m", default="service/default.jpg")
    price = models.FloatField()
    is_active = models.BooleanField(_('Active'), default=False,
                                    help_text=_('Activated, means Service will be published'))
    is_archived = models.BooleanField(_('Archive'), default=False,
                                      help_text=_('Archived, means Service will be Unpublished'))
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Salonist(CustomUser):
    pass

    class Meta:
        verbose_name = 'Salonist'
        verbose_name_plural = 'Salonist'


class SalonistProfile(Profile):
    user = models.OneToOneField(Salonist, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Salonist Profile'
        verbose_name_plural = 'Salonist Profile'


class SalonistFeedback(Feedback):
    user = models.ForeignKey(Salonist, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Salonist Feedback'
        verbose_name_plural = 'Salonist Feedback'


@receiver(post_save, sender=Salonist)
def salonist_profile(sender, instance, created, **kwargs):
    if created:
        SalonistProfile.objects.create(user=instance)
        instance.salonistprofile.save()
