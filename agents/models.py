from django.db import models


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
    def add(cls, agent_data, waypoint, faction):
        agent, created = cls.objects.update_or_create(
            symbol=agent_data['symbol'],
            defaults={
                'symbol': agent_data['symbol'],
                'headquarters': waypoint,
                'credit': agent_data['credits'],
                'starting_faction': faction,
                'ship_count': agent_data.get('shipCount'),
                'account_id': agent_data.get('accountId')
            }
        )
        return agent
