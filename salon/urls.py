from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="user/forgot-password.html",
             html_email_template_name="user/email/password-reset.html",
             subject_template_name="user/email/password_reset_subject.txt",
         ),
         name="password_reset"),
    path('reset_password_done/',
         auth_views.PasswordResetDoneView.as_view(template_name="user/password-reset-done.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="user/auth-reset-password.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="user/password-reset-complete.html"),
         name="password_reset_complete"),
    # ============================== Password Reset urls end ===========================================
    # third party app
    # path('mpesa/', include('mpesa_api.core.urls', 'mpesa')),

    path('admin/', admin.site.urls),
    path('finance/', include(('finance.urls', 'finance'), namespace="finance")),
    path('manager/', include(('manager.urls', 'manager'), namespace="project_manager")),
    path('salonist/', include(('salonist.urls', 'salonist'), namespace="salonist")),
    path('customer/', include(('customer.urls', 'customer'), namespace="customer")),
    path('trainee/', include(('trainee.urls', 'trainee'), namespace="trainee")),
    path('shipment/', include(('shipment.urls', 'shipment'), namespace="shipment")),
    path('stock/', include(('stock.urls', 'stock'), namespace="stock")),
    path('', include(('home.urls', 'home'), namespace="home")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'manager.views.error_404'
handler500 = 'manager.views.error_500'
handler403 = 'manager.views.error_403'
handler400 = 'manager.views.error_503'
