from django.db import models
from django.utils.translation import gettext_lazy as _


class Request(models.Model):
    """Custom model for requests

    The following model contains the request's id and received images

    Attributes:
        description (char): a picture's description
        picture (Image): a received picture to handle
    """

    description = models.CharField(
        max_length=100,
        default='no description',
        verbose_name=_('Description')
    )
    picture = models.ImageField(
        upload_to='photos',
        null=True,
        blank=True,
        verbose_name=_('Picture')
    )

    def __str__(self):
        return f'{self.id} ({self.description})'

    class Meta:
        verbose_name = _('Request')
        verbose_name_plural = _('Requests')
