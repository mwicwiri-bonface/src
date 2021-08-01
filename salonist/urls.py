from django.urls import path

from user.decorators import salonist_required
from . import views

urlpatterns = [
    path('confirm_order_payment/<int:order_id>/', salonist_required(views.confirm_order_payment),
         name="confirm_order_payment"),
    path('confirm_booking_payment/<int:booking_id>/', salonist_required(views.confirm_booking_payment),
         name="confirm_booking_payment"),
    path('search/', salonist_required(views.search), name="search"),
    path('feedback/', salonist_required(views.feedback), name="feedback"),
    path('password/', salonist_required(views.password_change), name="password_change"),
    path('faq/', salonist_required(views.faq), name="faq"),
    path('profile/', salonist_required(views.profile_main), name="profile_main"),
    path('schedule_appointment/', salonist_required(views.ScheduleAppointmentCreateView.as_view()),
         name="schedule_appointment"),
    path('appointment_list/', salonist_required(views.AppointmentListView.as_view()), name="appointment_list"),
    path('apprenticeship_list/', salonist_required(views.ApprenticeshipListView.as_view()), name="apprenticeship_list"),
    path('add_training/', salonist_required(views.TrainingCreateView.as_view()), name="add_training"),
    path('salonist_training/', salonist_required(views.TrainingListView.as_view()), name="salonist_training"),
    path('login/', views.login, name="login"),
    path('register/', views.SalonistSignUpView.as_view(), name="register"),
    path('verify/<uidb64>/<token>/', views.VerifyEmail.as_view(), name='verify'),
    path('', salonist_required(views.Home.as_view()), name="index"),
]
