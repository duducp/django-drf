from django.db import models

from marketplace.apps.models import BaseModel
from marketplace.apps.validators import only_letters_and_space


class Client(BaseModel):
    name = models.CharField(
        verbose_name='Name',
        max_length=50,
        validators=[only_letters_and_space]
    )
    last_name = models.CharField(
        verbose_name='Last Name',
        max_length=100,
        validators=[only_letters_and_space]
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True
    )

    @property
    def full_name(self) -> str:
        return f'{self.name} {self.last_name}'

    class Meta:
        app_label = 'clients'
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name
