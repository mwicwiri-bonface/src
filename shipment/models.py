from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import CustomUser, Profile, Feedback


class Agent(CustomUser):
    pass

    class Meta:
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'


class ShipmentLocations(models.Model):
    location = models.CharField(max_length=200)
    price = models.FloatField(default=0.0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Location: {self.location} :: Price {self.price}"


class AgentProfile(Profile):
    user = models.OneToOneField(Agent, on_delete=models.CASCADE)
    location = models.ForeignKey(ShipmentLocations, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Agent Profile'
        verbose_name_plural = 'Agents Profile'


class AgentFeedback(Feedback):
    user = models.ForeignKey(Agent, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Agent Feedback'
        verbose_name_plural = 'Agents Feedback'


@receiver(post_save, sender=Agent)
def agent_profile(sender, instance, created, **kwargs):
    if created:
        AgentProfile.objects.create(user=instance)
        instance.agentprofile.save()
