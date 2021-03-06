from django.urls import path

from user.decorators import customer_required
from . import views
from .receipts import OrderPaymentReceiptViewDownloadView

urlpatterns = [
    path('order-payment/<int:pk>/', customer_required(OrderPaymentReceiptViewDownloadView.as_view()),
         name="order_payment"),
    path('appointment/', customer_required(views.appointment), name="appointment"),
    path('service/<int:pk>/', customer_required(views.ServiceDetailView.as_view()), name="service-detail"),
    path('product/<slug>/', customer_required(views.ProductDetailView.as_view()), name="product-detail"),
    path('book_appointment/', customer_required(views.book_appointment), name="book_appointment"),
    path('generate_booking_receipt_pdf/<int:slug>/', customer_required(views.generate_booking_receipt_pdf),
         name="generate_booking_receipt_pdf"),
    path('generate_appointment_receipt_pdf/<int:slug>/', customer_required(views.generate_appointment_receipt_pdf),
         name="generate_appointment_receipt_pdf"),
    path('generate_order_receipt_pdf/<int:slug>/', customer_required(views.generate_order_receipt_pdf),
         name="generate_order_receipt_pdf"),
    path('generate_order_payment_receipt_pdf/<int:slug>/', customer_required(views.generate_order_payment_receipt_pdf),
         name="generate_order_payment_receipt_pdf"),
    path('generate_booking_payment_receipt_pdf/<int:slug>/', customer_required(views.booking_payment_receipt_pdf),
         name="generate_booking_payment_receipt_pdf"),
    path('book_hairstyle/<int:service_id>/', customer_required(views.book_hairstyle), name="book_hairstyle"),
    path('book_hairstyle/<int:service_id>/', customer_required(views.book_hairstyle), name="book_hairstyle"),
    path('booking_payment/<int:service_id>/', customer_required(views.booking_payment), name="booking_payment"),
    path('booking_checkout/', customer_required(views.booking_checkout), name="booking_checkout"),
    path('order_list/', customer_required(views.order_list), name="order_list"),
    path('checkout_pay/', customer_required(views.checkout_pay), name="checkout_pay"),
    path('checkout/', customer_required(views.checkout), name="checkout"),
    path('clear_cart/', customer_required(views.clear_cart), name="clear_cart"),
    path('increase_quantity/<slug>/', customer_required(views.increase_quantity), name="increase_quantity"),
    path('decrease_quantity/<slug>/', customer_required(views.decrease_quantity), name="decrease_quantity"),
    path('remove_from_cart/<slug>/', customer_required(views.remove_from_cart), name="remove_from_cart"),
    path('remove_from_wishlist/<slug>/', customer_required(views.remove_from_wishlist), name="remove_from_wishlist"),
    path('cart_list/', customer_required(views.cart_list), name="cart_list"),
    path('add_to_cart/<str:slug>/', customer_required(views.add_to_cart), name="add_to_cart"),
    path('add_to_wishlist/<str:slug>/', customer_required(views.add_to_wishlist), name="add_to_wishlist"),
    path('password_change/', customer_required(views.password_change), name="password_change"),
    path('change_password/', customer_required(views.change_password), name="change_password"),
    path('faq/', views.faq, name="faq"),
    path('wishlist_list/', customer_required(views.wishlist_list), name="wishlist_list"),
    path('profile/', customer_required(views.profile), name="profile"),
    path('profile_main/', customer_required(views.profile_main), name="profile_main"),
    path('add_booking/<int:slug>/', customer_required(views.add_booking), name="add_booking"),
    path('login/', views.login, name="login"),
    path('logout/', views.customer_logout, name="logout"),
    path('feedback_api/', customer_required(views.feedback_api), name="feedback_api"),
    path('feedback/', customer_required(views.feedback), name="feedback"),
    path('checkout/', customer_required(views.checkout), name="checkout"),
    # path('edit_billing/', views.edit_billing, name="edit_billing"),
    # path('favourites/', views.favourites, name="favourites"),
    # path('invoice_view/', views.invoice_view, name="invoice_view"),
    # path('invoices/', views.invoices, name="invoices"),
    # path('patient_profile/', views.patient_profile, name="patient_profile"),
    path('verify/<uidb64>/<token>/', views.VerifyEmail.as_view(), name="verify"),
    path('register/', views.CustomerSignUpView.as_view(), name="register"),
    # path('schedule_timings/', views.schedule_timings, name="schedule_timings"),
    path('apprenticeship_list/', customer_required(views.ApprenticeshipListView.as_view()), name="apprenticeship_list"),
    path('order_list/', customer_required(views.OrderListView.as_view()), name="order_list"),
    path('booking_list/', customer_required(views.BookingListView.as_view()), name="booking_list"),
    path('', customer_required(views.Home.as_view()), name="index"),
]
