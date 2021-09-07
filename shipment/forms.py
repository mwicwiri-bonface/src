from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Agent, AgentProfile, AgentFeedback, ShipmentLocations


class AgentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Agent
        fields = ['last_name', 'first_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        user.is_active = False
        if commit:
            user.save()
        return user


class AgentProfileForm(ModelForm):
    class Meta:
        model = AgentProfile
        fields = ['image', 'gender', 'phone_number', 'location']


class AgentForm(ModelForm):
    class Meta:
        model = Agent
        fields = ['last_name', 'first_name', 'email']


class AgentFeedbackForm(ModelForm):
    class Meta:
        model = AgentFeedback
        fields = ['subject', 'message']


class ShipmentLocationsForm(ModelForm):
    class Meta:
        model = ShipmentLocations
        fields = ['location', 'price']

