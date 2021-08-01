from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Stock, StockProfile, StockFeedback


class StockSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Stock
        fields = ['last_name', 'first_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_stock = True
        user.is_active = False
        if commit:
            user.save()
        return user


class StockProfileForm(ModelForm):
    class Meta:
        model = StockProfile
        fields = ['image', 'gender', 'phone_number']


class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['last_name', 'first_name', 'email']


class StockFeedbackForm(ModelForm):
    class Meta:
        model = StockFeedback
        fields = ['subject', 'message']
