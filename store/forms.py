from django.forms import ModelForm

from store.models import Product, Gallery, Review, OrderItem, OrderPayment


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['discount', 'name', 'price', 'image', 'description', 'quantity']


class GalleryForm(ModelForm):
    class Meta:
        model = Gallery
        fields = ['image']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'review', 'rating']


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderPaymentForm(ModelForm):
    class Meta:
        model = OrderPayment
        fields = ['mpesa', 'phone', 'amount']
