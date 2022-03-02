from django.db import models
from django.utils.translation import gettext as _
from accounts.models import User

# Create your models here.
class UserLobby(models.Model):
    name = models.CharField(_('lobby name'), max_length=300)
    img = models.ImageField(_('lobby image'), upload_to="uploads/%y/%m/%d", blank=True)
    thumbnail = models.ImageField(_('lobby thumbnail'), upload_to="uploads/%y/%m/%d", blank=True)
    followers_count = models.IntegerField(_('lobby followers count'), blank=True, default=0)
    users = models.ManyToManyField(User, related_name='+')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(_('lobby created on'), auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

