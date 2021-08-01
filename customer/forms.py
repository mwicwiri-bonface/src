from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Customer, CustomerProfile, CustomerFeedback


class CustomerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = ['last_name', 'first_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        user.is_active = False
        if commit:
            user.save()
        return user


class CustomerProfileForm(ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['image', 'gender', 'phone_number', 'location']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['last_name', 'first_name', 'email']


class CustomerFeedbackForm(ModelForm):
    class Meta:
        model = CustomerFeedback
        fields = ['subject', 'message']

