from django.urls import path

from user.decorators import finance_required
from . import views

urlpatterns = [
    path('confirm_order_payment/<int:order_id>/', finance_required(views.confirm_order_payment),
         name="confirm_order_payment"),
    path('confirm_booking_payment/<int:booking_id>/', finance_required(views.confirm_booking_payment),
         name="confirm_booking_payment"),
    path('confirm_training_payment/<int:slug>/', finance_required(views.confirm_training_payment),
         name="confirm_training_payment"),
    path('search/', finance_required(views.search), name="search"),
    path('feedback/', finance_required(views.feedback), name="feedback"),
    path('password/', finance_required(views.password_change), name="password_change"),
    path('faq/', finance_required(views.faq), name="faq"),
    path('profile/', finance_required(views.profile_main), name="profile_main"),
    path('booking_payment/', finance_required(views.BookingPaymentListView.as_view()),
         name="booking_payment"),
    path('pending_booking_payment/', finance_required(views.PendingBookingPaymentListView.as_view()),
         name="pending_booking_payment"),
    path('order_payment/', finance_required(views.OrderPaymentListView.as_view()), name="order_payment"),
    path('pending_order_payment/', finance_required(views.PendingOrderPaymentListView.as_view()),
         name="pending_order_payment"),
    path('pending_payment/', finance_required(views.PendingTrainingPaymentListView.as_view()), name="pending_payment"),
    path('payment/', finance_required(views.TrainingPaymentListView.as_view()), name="payment"),
    path('login/', views.login, name="login"),
    path('register/', views.FinanceSignUpView.as_view(), name="register"),
    path('verify/<uidb64>/<token>/', views.VerifyEmail.as_view(), name='verify'),
    path('', finance_required(views.Home.as_view()), name="index"),
]
