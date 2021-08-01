from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Finance, FinanceProfile, FinanceFeedback


class FinanceSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Finance
        fields = ['last_name', 'first_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_finance = True
        user.is_active = False
        if commit:
            user.save()
        return user


class FinanceProfileForm(ModelForm):
    class Meta:
        model = FinanceProfile
        fields = ['image', 'gender', 'phone_number']


class FinanceForm(ModelForm):
    class Meta:
        model = Finance
        fields = ['last_name', 'first_name', 'email']


class FinanceFeedbackForm(ModelForm):
    class Meta:
        model = FinanceFeedback
        fields = ['subject', 'message']

