import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.dispatch import receiver
from django.contrib.auth import user_logged_in, user_logged_out



class UserManager(BaseUserManager):
    '''
    creating a manager for a custom user model
    '''
    def create_user(self, email, password=None):
        """
        Create and return a `User` with an email, username and password.
        """
        if not email:
            raise ValueError('Users Must Have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Create and return a User with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
        )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        return self.email

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


class EmailOTP(models.Model):
    otp = models.CharField(max_length=6)
    email = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    session = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.otp



class LoggedInUser(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name='logged_in_user')
    session_key = models.CharField(max_length=32, null=True, blank=True)  # Session keys are 32 characters long

    def __str__(self):
        return self.user.email



@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    # print("on_user_logged_in")
    LoggedInUser.objects.get_or_create(user=kwargs.get('user')) 


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    # print("on_user_logged_out")
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()
        