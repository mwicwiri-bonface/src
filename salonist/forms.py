from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Salonist, SalonistProfile, SalonistFeedback


class SalonistSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Salonist
        fields = ['last_name', 'first_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_salonist = True
        user.is_active = False
        if commit:
            user.save()
        return user


class SalonistProfileForm(ModelForm):
    class Meta:
        model = SalonistProfile
        fields = ['image', 'gender', 'phone_number', 'service']


class SalonistForm(ModelForm):
    class Meta:
        model = Salonist
        fields = ['last_name', 'first_name', 'email']


class SalonistFeedbackForm(ModelForm):
    class Meta:
        model = SalonistFeedback
        fields = ['subject', 'message']
