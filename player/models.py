from django.contrib.auth.models import AbstractUser
from django.db import models


class Player(AbstractUser):
    token = models.CharField(
        max_length=600,
        unique=True,
        null=True,
        blank=True,
        help_text='SpaceTraders API token for this player.'
    )
    agent = models.OneToOneField(
        'agents.Agent',
        related_name='django_player',
        on_delete=models.CASCADE,
        null=True,
        help_text='The symbol of the SpaceTraders agent associated with this player.'
    )
