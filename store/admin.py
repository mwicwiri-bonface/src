from django.contrib import admin, messages
from django.utils.translation import ngettext
from .models import Product, Gallery, Review, Order, OrderItem, OrderPayment, Wishlist


class GalleryInline(admin.TabularInline):
    model = Gallery


class ProductAdmin(admin.ModelAdmin):
    inlines = [GalleryInline, ]
    list_display = ('name', 'price', 'image', 'description', 'quantity', 'discount')
    search_fields = ('name', 'description',)
    list_filter = ('is_discount', 'is_active', 'is_archived', 'updated', 'created')

    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True, is_archived=False)
        self.message_user(request, ngettext(
            '%d Product has successfully been marked as active.',
            '%d Products have been successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    make_active.short_description = "Approve Product"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_archived=True)
        self.message_user(request, ngettext(
            '%d Product has been archived successfully.',
            '%d Products have been archived successfully.',
            updated,
        ) % updated, messages.INFO)

    make_inactive.short_description = "Archive Product"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'created', 'updated')
    list_filter = ('updated', 'created')

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'review', 'rating')
    search_fields = ('review',)
    list_filter = ('updated', 'created')

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class OrderAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'customer', 'completed', 'is_active')
    search_fields = ('transaction_id',)
    list_filter = ('completed', 'is_active', 'is_archived', 'updated', 'created')

    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True, is_archived=False)
        self.message_user(request, ngettext(
            '%d Order has successfully been marked as active.',
            '%d Orders have been successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    make_active.short_description = "Approve Order"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_archived=True)
        self.message_user(request, ngettext(
            '%d Order has been archived successfully.',
            '%d Orders have been archived successfully.',
            updated,
        ) % updated, messages.INFO)

    make_inactive.short_description = "Archive Order"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    list_filter = ('updated', 'created')

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class OrderPaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'mpesa', 'phone', 'amount', 'manager', 'confirmed')
    search_fields = ('mpesa', 'phone',)
    list_filter = ('confirmed', 'updated', 'created')

    actions = ['confirmed']

    def confirmed(self, request, queryset):
        updated = queryset.update(confirmed=True)
        self.message_user(request, ngettext(
            '%d Order Payment has successfully been marked as confirmed.',
            '%d Order Payments have been successfully marked as confirmed.',
            updated,
        ) % updated, messages.SUCCESS)

    confirmed.short_description = "Approve Order Payment"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


admin.site.register(Product, ProductAdmin)
admin.site.register(Wishlist)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderPayment, OrderPaymentAdmin)
