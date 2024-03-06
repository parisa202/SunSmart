from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Custom User manger for User model
class CoreUserManager(BaseUserManager):
    """Define a model manager for CoreUser model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CoreUser(AbstractUser):
    """CoreUser  Model, which is the basic and initial information of the User.
        The other User information will be defined in other Apps.
    """

    username = None
    first_name = None
    last_name = None
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,db_index=True,)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CoreUserManager()

    # def get_absolute_url(self):
    #     return reverse('resumeApp:resume', args=[self.id])

    # def get_absolute_url(self):
    #     return reverse('resumeApp:personal-resume-private', kwargs={'user_id':self.id,
    #                                                             'full_name':self.slug})

    def get_full_name(self):
        return self.email

    def get_short_name(self):
         return self.email

    def __unicode__(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
