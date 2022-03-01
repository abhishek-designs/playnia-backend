from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token
from .managers import UserManager

# Create your models here.
class User(AbstractUser):
    """
        Our custom user model in which username is not required
    """
    username = None
    email = models.EmailField(_('email id'), unique=True)
    bio = models.TextField(_('user bio'), blank=True)
    followers = models.IntegerField(_('followers'), blank=True, default=0)
    following = models.IntegerField(_('following'),blank=True, default=0)
    total_questions = models.IntegerField(_('total questions'), blank=True, default=0)
    total_answers = models.IntegerField(_('total answers'), blank=True, default=0)
    profile_pic = models.ImageField(_('profile pic'), blank=True, null=True, upload_to='uploads/%y/%m/%d')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        """
            Automatically generate token for user on registration
        """
        if created:
            Token.objects.create(user=instance)
    
