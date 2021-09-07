from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import CustomUser, Profile, Feedback


class Manager(CustomUser):
    pass

    class Meta:
        verbose_name = ' Manager'
        verbose_name_plural = ' Managers'


class ManagerProfile(Profile):
    user = models.OneToOneField(Manager, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ' Manager Profile'
        verbose_name_plural = ' Managers Profile'


class ManagerFeedback(Feedback):
    user = models.ForeignKey(Manager, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ' Manager'
        verbose_name_plural = ' Manager Feedback'


@receiver(post_save, sender=Manager)
def manager_profile(sender, instance, created, **kwargs):
    if created:
        ManagerProfile.objects.create(user=instance)
        instance.managerprofile.save()

