from django.contrib.auth.models import AbstractUser
from django.db import models

from factions.models import Faction
from systems.models import Waypoint

class User(AbstractUser):
    token = models.CharField(
        max_length=600,
        unique=True,
        null=True,
        blank=True,
        help_text='SpaceTraders API token for this user.'
    )
    agent = models.OneToOneField(
        'Agent',
        related_name='django_user',
        on_delete=models.CASCADE,
        null=True,
        help_text='The symbol of the SpaceTraders agent associated with this user.'
    )


class Agent(models.Model):
    symbol = models.CharField(
        primary_key=True,
        max_length=14
    )
    headquarters = models.ForeignKey(
        'systems.Waypoint',
        on_delete=models.CASCADE,
        related_name='agent_headquarters',
        # Only to be able to start adding the faction mock agents.
        null=True
    )
    credit = models.BigIntegerField(
        help_text="The number of credits the agent has available. Credits can be negative if funds have been overdrawn."
    )
    starting_faction = models.ForeignKey(
        'factions.Faction',
        on_delete=models.CASCADE,
        # Only to be able to start adding the faction mock agents.
        null=True
    )
    ship_count = models.IntegerField(
        null=True,
        blank=True
    )
    account_id = models.CharField(
        max_length=500,
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Agent {self.symbol} with {self.credit} credits.'

    @classmethod
    def add(cls, agent_data):
        agent, created = cls.objects.update_or_create(
            symbol=agent_data['symbol'],
            headquarters=Waypoint.objects.filter(symbol=agent_data['headquarters']).first(),
            credit=agent_data['credits'],
            starting_faction=Faction.objects.filter(symbol=agent_data['startingFaction']).first(),
            ship_count=agent_data.get('shipCount'),
            account_id=agent_data.get('accountId')
        )
        return agent
