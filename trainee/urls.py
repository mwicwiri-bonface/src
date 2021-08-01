from django.urls import path

from user.decorators import trainee_required
from . import views

urlpatterns = [
    path('feedback/', trainee_required(views.feedback), name="feedback"),
    path('change_password/', trainee_required(views.change_password), name="change_password"),
    path('apply_training/', trainee_required(views.apply_training), name="apply_training"),
    path('training_payment/', trainee_required(views.training_payment), name="training_payment"),
    path('pending_training/', trainee_required(views.PendingTrainingListView.as_view()), name="pending_training"),
    path('training/', trainee_required(views.TrainingListView.as_view()), name="training"),
    path('pending_payment/', trainee_required(views.PendingTrainingPaymentListView.as_view()), name="pending_payment"),
    path('payment/', trainee_required(views.TrainingPaymentListView.as_view()), name="payment"),
    path('faq/', views.faq, name="faq"),
    path('profile/', trainee_required(views.profile), name="profile"),
    path('login/', views.login, name="login"),
    path('verify/<uidb64>/<token>/', views.VerifyEmail.as_view(), name="verify"),
    path('register/', views.TraineeSignUpView.as_view(), name="register"),
    path('', trainee_required(views.Home.as_view()), name="index"),
]
