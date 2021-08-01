import functools
import ssl

from django.conf import settings
from django.utils import timezone
from django.views.generic import DetailView

from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.utils import django_url_fetcher
from django_weasyprint.views import CONTENT_TYPE_PNG, WeasyTemplateResponse, CONTENT_TYPE_PDF

from store.models import OrderPayment


class OrderPaymentReceiptView(DetailView):
    # vanilla Django DetailView
    model = OrderPayment
    template_name = 'customer/receipts/invoice-view.html'


class CustomWeasyTemplateResponse(WeasyTemplateResponse):
    # customized response class to change the default URL fetcher
    def get_url_fetcher(self):
        # disable host and certificate check
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return functools.partial(django_url_fetcher, ssl_context=context)


class OrderPaymentPrintView(WeasyTemplateResponseMixin, OrderPaymentReceiptView):
    # output of MyModelView rendered as PDF with hardcoded CSS
    pdf_stylesheets = [
        settings.STATIC_ROOT + 'customer/assets/css/bootstrap.min.css',
        settings.STATIC_ROOT + 'customer/assets/plugins/fontawesome/css/fontawesome.min.css',
        settings.STATIC_ROOT + 'customer/assets/plugins/fontawesome/css/all.min.css',
        settings.STATIC_ROOT + 'customer/assets/css/style.css',
    ]
    pdf_scripts = [
        settings.STATIC_ROOT + 'customer/assets/js/jquery.min.js',
        settings.STATIC_ROOT + 'customer/assets/js/popper.min.js',
        settings.STATIC_ROOT + 'customer/assets/js/bootstrap.min.js',
        settings.STATIC_ROOT + 'customer/assets/js/script.js',
    ]
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = False
    # custom response class to configure url-fetcher
    response_class = CustomWeasyTemplateResponse


class OrderPaymentReceiptViewDownloadView(WeasyTemplateResponseMixin, OrderPaymentReceiptView):
    # suggested filename (is required for attachment/download!)
    pdf_filename = 'foo.pdf'


class OrderPaymentReceiptViewImageView(WeasyTemplateResponseMixin, OrderPaymentReceiptView):
    # generate a PNG image instead
    content_type = CONTENT_TYPE_PNG

    # dynamically generate filename
    def get_pdf_filename(self):
        return 'foo-{at}.pdf'.format(
            at=timezone.now().strftime('%Y%m%d-%H%M'),
        )
