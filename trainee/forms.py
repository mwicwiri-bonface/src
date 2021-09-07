from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Trainee, TraineeProfile, TraineeFeedback, Training, TrainingApplication, TrainingPayment


class TraineeSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Trainee
        fields = ['last_name', 'first_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_trainee = True
        user.is_active = False
        if commit:
            user.save()
        return user


class TraineeProfileForm(ModelForm):
    class Meta:
        model = TraineeProfile
        fields = ['image', 'gender', 'phone_number']


class TraineeForm(ModelForm):
    class Meta:
        model = Trainee
        fields = ['last_name', 'first_name', 'email']


class TraineeFeedbackForm(ModelForm):
    class Meta:
        model = TraineeFeedback
        fields = ['subject', 'message']


class TrainingForm(ModelForm):
    class Meta:
        model = Training
        fields = ['service', 'price', 'date', 'end_date']


class TrainingApplicationForm(ModelForm):
    class Meta:
        model = TrainingApplication
        fields = ['training']


class TrainingPaymentForm(ModelForm):
    class Meta:
        model = TrainingPayment
        fields = ['training', 'amount', 'mpesa']
