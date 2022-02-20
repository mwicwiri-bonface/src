from django.urls import path

from user.decorators import manager_required
from . import views

urlpatterns = [
    path('add_training/', manager_required(views.TrainingCreateView.as_view()), name="add_training"),
    path('confirm_training_application/<int:application_id>/', manager_required(views.confirm_training_application),
         name="confirm_training_application"),
    path('approved_training_application_pdf/', manager_required(views.approved_training_application_pdf),
         name="approved_training_application_pdf"),
    path('pending_training_application_pdf/', manager_required(views.pending_training_application_pdf),
         name="pending_training_application_pdf"),
    path('pending_training_pdf/', manager_required(views.pending_training_pdf), name="pending_training_pdf"),
    path('training_pdf/', manager_required(views.training_pdf), name="training_pdf"),
    path('salonists_pdf/', manager_required(views.salonists_pdf), name="salonists_pdf"),
    path('products_pdf/', manager_required(views.products_pdf), name="products_pdf"),
    path('manager_training_application/', manager_required(views.ApprovedTrainingApplicationListView.as_view()),
         name="manager_training_application"),
    path('manager_pending_training_application/', manager_required(views.PendingTrainingApplicationListView.as_view()),
         name="manager_pending_training_application"),
    path('manager_training/', manager_required(views.TrainingListView.as_view()), name="manager_training"),
    path('manager_pending/', manager_required(views.PendingTrainingListView.as_view()),
         name="pending_manager_training"),
    path('search/', manager_required(views.search), name="search"),
    path('feedback/', manager_required(views.feedback), name="feedback"),
    path('password/', manager_required(views.password_change), name="password_change"),
    path('faq/', manager_required(views.faq), name="faq"),
    path('profile/', manager_required(views.profile_main), name="profile_main"),
    path('create_salonist_service/', manager_required(views.SalonistServiceCreateView.as_view()),
         name="create_salonist_service"),
    path('salonist_service_list/', manager_required(views.SalonistServiceListView.as_view()),
         name="salonist_service_list"),
    path('apprenticeships/', manager_required(views.ApprenticeshipListView.as_view()), name="apprenticeships"),
    path('create-apprenticeship/', manager_required(views.ApprenticeshipCreateView.as_view()),
         name="create_apprenticeship"),
    path('create-salonist/', manager_required(views.SalonistCreateView.as_view()), name="create_salonist"),
    path('create-product/', manager_required(views.ProductCreateView.as_view()), name="create_product"),
    path('create-service/', manager_required(views.ServiceCreateView.as_view()), name="create_service"),
    path('services/', manager_required(views.ServicesListView.as_view()), name="services"),
    path('products/', manager_required(views.ProductsListView.as_view()), name="products"),
    path('salonists/', manager_required(views.SalonistsListView.as_view()), name="salonists"),
    path('customers/', manager_required(views.CustomersListView.as_view()), name="customers"),
    path('login/', views.login, name="login"),
    path('register/', views.ManagerSignUpView.as_view(), name="register"),
    path('verify/<uidb64>/<token>/', views.VerifyEmail.as_view(), name='verify'),
    path('', manager_required(views.Home.as_view()), name="index"),
]