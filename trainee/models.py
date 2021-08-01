from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from finance.models import Finance
from salonist.models import Salonist
from service.models import Service
from user.models import CustomUser, Profile, Feedback


class Trainee(CustomUser):
    pass

    class Meta:
        verbose_name = 'Trainee'
        verbose_name_plural = 'Trainees'


class TraineeProfile(Profile):
    user = models.OneToOneField(Trainee, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Trainee Profile'
        verbose_name_plural = 'Trainees Profile'


class TraineeFeedback(Feedback):
    user = models.ForeignKey(Trainee, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Trainee Feedback'
        verbose_name_plural = 'Trainees Feedback'


class Training(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    salonist = models.ForeignKey(Salonist, on_delete=models.CASCADE)
    price = models.FloatField(default=0.0)
    date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.name}"


class TrainingApplication(models.Model):
    code = models.CharField(max_length=200)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.training} :: {self.trainee.get_full_name} :: {self.code}"


class TrainingPayment(models.Model):
    code = models.CharField(max_length=200)
    training = models.ForeignKey(TrainingApplication, on_delete=models.CASCADE)
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, null=True, blank=True)
    finance = models.ForeignKey(Finance, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField(default=0.0)
    mpesa = models.CharField(max_length=100)
    is_confirmed = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"mpesa code : {self.mpesa} :: amount {str(self.amount)}"


@receiver(post_save, sender=Trainee)
def trainee_profile(sender, instance, created, **kwargs):
    if created:
        TraineeProfile.objects.create(user=instance)
        instance.traineeprofile.save()
