from autoslug import AutoSlugField
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from customer.models import Customer
from finance.models import Finance
from .utils import generate_code

PERCENT_DISCOUNT = (
    (0.05, '95 %'),
    (0.10, '90 %'),
    (0.15, '85 %'),
    (0.20, '80 %'),
    (0.25, '75 %'),
    (0.30, '70 %'),
    (0.35, '65 %'),
    (0.40, '60 %'),
    (0.45, '55 %'),
    (0.50, '50 %'),
    (0.55, '45 %'),
    (0.60, '40 %'),
    (0.65, '35 %'),
    (0.70, '30 %'),
    (0.75, '25 %'),
    (0.80, '20 %'),
    (0.85, '15 %'),
    (0.90, '10 %'),
    (0.95, '5 %'),
    (1.0, '0 %'),
)


class Product(models.Model):
    slug = AutoSlugField(populate_from='slug_name')
    discount = models.FloatField(default=1.0, choices=PERCENT_DISCOUNT)
    name = models.CharField(max_length=150)
    price = models.FloatField()
    image = models.ImageField(upload_to='product/images/%Y/%m/%d/', null=True)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
    is_discount = models.BooleanField(_('Discount'), default=False,
                                      help_text=_('when active, discount will be applied'))
    is_active = models.BooleanField(_('Active'), default=False, help_text=_('Activated, allow to publish'))
    is_archived = models.BooleanField(_('Archived'), default=False, help_text=_('Activated, gets unpublished'))
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)

    class Meta:
        ordering = ["-created"]

    @property
    def gallery(self):
        return self.gallery_set.all().order_by('-timestamp')

    @property
    def reviews_rating(self):
        review_total = 0
        number_of_reviews = 0
        reviews_all = self.productreview_set.all()
        for review in reviews_all:
            if review.rating is not None:
                review_rating = review.rating
                review_total += review_rating
                number_of_reviews += 1
        average_rating = review_total // number_of_reviews
        return average_rating

    @property
    def image_url(self):
        return self.image.url

    @property
    def slug_name(self):
        s = "-"
        seq = (generate_code(5, 5), self.name)  # This is sequence of strings.
        slug = s.join(seq)
        return slug

    def __str__(self):
        return f"{self.name}"


class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product/%y/%m", default="product/default.jpg")
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(default=0)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)


class Order(models.Model):
    transaction_id = models.CharField(max_length=250)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    completed = models.BooleanField(_('Completed'), default=False)
    is_active = models.BooleanField(_('Active'), default=False)  # true means complete
    is_archived = models.BooleanField(_('Archived'), default=False,
                                      help_text=_('Means the oder has been cancelled.'))  # order cancelled
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = (sum([item.get_total for item in order_items]))
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = (sum([item.quantity for item in order_items]))
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    # is_active = models.BooleanField(_('Active'), default=False)
    # is_archived = models.BooleanField(_('Archived'), default=False, help_text=_('Activated, gets unpublished'))
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)

    @property
    def get_price(self):
        price = self.product.price * self.product.discount
        return price

    @property
    def get_total(self):
        total = self.get_price * self.quantity
        return total


class OrderPayment(models.Model):
    transaction_id = models.CharField(max_length=250)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    mpesa = models.CharField(max_length=10, help_text="Mpesa Code e.g MXFTR432R5")
    phone = PhoneNumberField(blank=True, null=True)
    manager = models.ForeignKey(Finance, on_delete=models.CASCADE, null=True)
    amount = models.FloatField(default=0.0)
    confirmed = models.BooleanField(default=False, help_text="Means manager has confirmed payment")
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)


class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.BooleanField(default=False, help_text="means product is in cart")
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
