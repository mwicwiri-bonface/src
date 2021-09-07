from django.urls import path

from user.decorators import stock_required
from . import views

urlpatterns = [
    path('search/', stock_required(views.search), name="search"),
    path('feedback/', stock_required(views.feedback), name="feedback"),
    path('password/', stock_required(views.password_change), name="password_change"),
    path('faq/', stock_required(views.faq), name="faq"),
    path('profile/', stock_required(views.profile_main), name="profile_main"),
    path('create-product/', stock_required(views.ProductCreateView.as_view()), name="create_product"),
    path('add_product_gallery/<slug>/', stock_required(views.add_product_gallery), name="add_product_gallery"),
    path('products/', stock_required(views.ProductsListView.as_view()), name="products"),
    path('login/', views.login, name="login"),
    path('register/', views.StockSignUpView.as_view(), name="register"),
    path('', stock_required(views.Home.as_view()), name="index"),
]
