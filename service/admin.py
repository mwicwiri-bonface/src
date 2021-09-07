from django.contrib import admin, messages
from django.utils.translation import ngettext
from .models import Service, SalonistService, Booking, BookingPayment, Appointment, Apprenticeship, \
    ApprenticeshipApplication


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image', 'price')
    search_fields = ('name', 'description',)
    list_filter = ('is_active', 'is_archived', 'updated', 'created')

    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True, is_archived=False)
        self.message_user(request, ngettext(
            '%d Service has successfully been marked as active.',
            '%d Services have been successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    make_active.short_description = "Approve Service"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_archived=True)
        self.message_user(request, ngettext(
            '%d Service has been archived successfully.',
            '%d Services have been archived successfully.',
            updated,
        ) % updated, messages.INFO)

    make_inactive.short_description = "Archive Service"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class SalonistServiceAdmin(admin.ModelAdmin):
    list_display = ('salonist', 'service', 'is_active', 'created', 'updated')
    list_filter = ('is_active', 'is_archived', 'updated', 'created')
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True, is_archived=False)
        self.message_user(request, ngettext(
            '%d Salonist Service has been successfully marked as active.',
            '%d Salonist Services have been successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    make_active.short_description = "Mark selected Salonist Services as active"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_archived=True)
        self.message_user(request, ngettext(
            '%d Salonist Service has been successfully marked as inactive.',
            '%d Salonist Services has been successfully marked as inactive.',
            updated,
        ) % updated)

    make_inactive.short_description = "Mark selected Salonist Services as inactive"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class BookingAdmin(admin.ModelAdmin):
    list_display = ('service', 'customer', 'is_paid', 'created', 'updated')
    list_filter = ('is_active', 'is_paid', 'updated', 'created')
    actions = ['paid']

    def paid(self, request, queryset):
        updated = queryset.update(is_paid=True)
        self.message_user(request, ngettext(
            '%d Booking has been successfully marked as paid.',
            '%d Bookings have been successfully marked as paid.',
            updated,
        ) % updated, messages.SUCCESS)

    paid.short_description = "Mark selected Bookings as paid"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class BookingPaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'mpesa', 'phone', 'confirmed')
    search_fields = ('mpesa', 'phone',)
    list_filter = ('confirmed', 'manager', 'updated', 'created')

    actions = ['confirmed']

    def confirmed(self, request, queryset):
        updated = queryset.update(confirmed=True)
        self.message_user(request, ngettext(
            '%d Booking Payment has successfully been marked as active.',
            '%d Booking Payments have been successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    confirmed.short_description = "Approve Booking Payment"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'salonist', 'date', 'completed')
    list_filter = ('completed', 'date', 'updated', 'created')

    actions = ['completed']

    def completed(self, request, queryset):
        updated = queryset.update(completed=True)
        self.message_user(request, ngettext(
            '%d Appointment has successfully been marked as active.',
            '%d Appointments have been successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    completed.short_description = "Approve Appointment"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class ApprenticeshipAdmin(admin.ModelAdmin):
    list_display = ('salonist', 'date', 'is_active')
    list_filter = ('date', 'is_active', 'is_archived', 'updated', 'created')

    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True, is_archived=False)
        self.message_user(request, ngettext(
            '%d Apprenticeship has successfully been marked as active.',
            '%d Apprenticeships have been successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    make_active.short_description = "Approve Apprenticeship"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_archived=True)
        self.message_user(request, ngettext(
            '%d Apprenticeship has been archived successfully.',
            '%d Apprenticeships have been archived successfully.',
            updated,
        ) % updated, messages.INFO)

    make_inactive.short_description = "Archive Apprenticeship"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class ApprenticeshipApplicationAdmin(admin.ModelAdmin):
    list_display = ('program', 'customer', 'attended')
    list_filter = ('attended', 'updated', 'created')

    actions = ['attended']

    def attended(self, request, queryset):
        updated = queryset.update(attended=True)
        self.message_user(request, ngettext(
            '%d Application has successfully been marked as attended.',
            '%d Applications have been successfully marked as attended.',
            updated,
        ) % updated, messages.SUCCESS)

    attended.short_description = "Approve Application"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


admin.site.register(Service, ServiceAdmin)
admin.site.register(SalonistService, SalonistServiceAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(BookingPayment, BookingPaymentAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Apprenticeship, ApprenticeshipAdmin)
admin.site.register(ApprenticeshipApplication, ApprenticeshipApplicationAdmin)
