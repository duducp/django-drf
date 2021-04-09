from django.db import models

from project.apps.models import BaseModel


class Favorite(BaseModel):
    product_id = models.UUIDField(
        verbose_name='Product Id',
    )
    client = models.ForeignKey(
        verbose_name='Client',
        to='clients.Client',
        related_name='favorite_client',
        on_delete=models.PROTECT
    )

    class Meta:
        app_label = 'favorites'
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        ordering = ['-created_at']
        unique_together = ('product_id', 'client',)
