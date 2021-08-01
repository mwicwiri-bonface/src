from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Manager, ManagerProfile, Feedback, ManagerFeedback


class ManagerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Manager
        fields = ['last_name', 'first_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_manager = True
        user.is_active = False
        if commit:
            user.save()
        return user


class ManagerProfileForm(ModelForm):
    class Meta:
        model = ManagerProfile
        fields = ['image', 'gender', 'phone_number']


class ManagerForm(ModelForm):
    class Meta:
        model = Manager
        fields = ['last_name', 'first_name', 'email']


class ManagerFeedbackForm(ModelForm):
    class Meta:
        model = ManagerFeedback
        fields = ['subject', 'message']
