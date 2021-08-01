import autoslug
from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager

GENDER_TYPES = (
    ('m', 'Male'),
    ('f', 'Female')
)


class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom user model."""

    def create_user(self, email, username, password=None):
        """Creates a user profile object."""

        if not email:
            raise ValueError('Users must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)

        user.user_id = -1
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        """Creates and saves a new superuser with given details."""

        user = self.create_user(email=email, username=username, password=password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)


class CustomUser(AbstractUser):
    slug = autoslug.AutoSlugField(populate_from='email')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(_('email'), unique=True, help_text="User will be able to login using email")
    username = models.CharField(max_length=100, null=True)
    is_staff = models.BooleanField(default=False, help_text="Used for super user authentications")
    is_superuser = models.BooleanField(default=False, help_text="Means user is admin")
    is_customer = models.BooleanField(default=False, help_text="Means user can login to customer's portal")
    is_manager = models.BooleanField(default=False, help_text="Means user can login to manager's portal")
    is_salonist = models.BooleanField(default=False, help_text="Means user can login to salonist portal")
    is_finance = models.BooleanField(default=False, help_text="Means user can login to finance portal")
    is_agent = models.BooleanField(default=False, help_text="Means user can login to Shipment Agent's portal")
    is_stock = models.BooleanField(default=False, help_text="Means user can login to Stock Manager's portal")
    is_trainee = models.BooleanField(default=False, help_text="Means user can login to Apprenticeship portal")
    is_active = models.BooleanField(default=True, help_text="Means user can login to the system")
    is_archived = models.BooleanField(default=False, help_text="Means User cannot login")
    is_verified = models.BooleanField(default=False, help_text="Means email is valid")
    is_approved = models.BooleanField(default=False, help_text="Means that user has been approved")
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True,
                                   help_text="means last time table instance was edited")
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True,
                                   help_text="time table instance was created")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.email}'

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def _allow_edit(obj=None):
        if not obj:
            return True
        return not (obj.is_superuser or obj.staff)

    def has_perm(self, request, obj=None):
        return True


class Profile(models.Model):
    image = models.ImageField(upload_to='Users/Customers/profile_pictures/%Y/%m/',
                              default="Users/profile_pictures/default.jpg")
    gender = models.CharField(
        choices=GENDER_TYPES,
        default='m',
        max_length=2,
        null=True,
        blank=True
    )
    phone_number = PhoneNumberField(blank=True, null=True)
    is_active = models.BooleanField(_('Active'), default=False, help_text=_('Activated, users profile is published'))
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)


class Feedback(models.Model):
    slug = AutoSlugField(populate_from='subject')
    subject = models.CharField(max_length=200)
    message = models.TextField(help_text="Feedback sent by users to admin")
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="admin", null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.subject}"

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'


# signal to send an email to the admin when a user creates a new account
@receiver(post_save, sender=CustomUser, dispatch_uid='register')
def register(sender, instance, **kwargs):
    if kwargs.get('created', False):
        subject = 'Verification of the %s account' % instance.get_full_name
        message = 'A new user has registered'
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, [from_email], fail_silently=False)


# automatically sends mail to applicant when they click apply button
@receiver(post_save, sender=Feedback)
def feedback(sender, instance, created, **kwargs):
    if created:
        print(instance.admin.email)
        to_email = instance.admin.email
        subject = instance.subject
        msg_plain = render_to_string('applicant/emails/feedback.txt', {'message': instance.message, })
        msg_html = render_to_string('applicant/emails/feedback.html', {
            'instance': instance,
        })
        send_mail(subject, msg_plain, 'Varal Software Trainee', [to_email], html_message=msg_html)

