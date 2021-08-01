from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name="search"),
    path('term_condition/', views.term_condition, name="term_condition"),
    path('privacy-policy/', views.privacy_policy, name="privacy_policy"),
    path('salonists/', views.Salonists.as_view(), name="salonists"),
    path('', views.Home.as_view(), name="index"),
]
