from django.db import models

from factions.models import Faction
from systems.models import Waypoint
from systems.models import TradeGood


CONTRACT_TYPES = [
    ('PROCUREMENT', 'Procurement'),
    ('TRANSPORT', 'Transport'),
    ('SHUTTLE', 'Shuttle')
]


class Contract(models.Model):
    contract_id = models.CharField(
        primary_key=True,
        max_length=500
    )
    faction = models.ForeignKey(
        'factions.Faction',
        on_delete=models.CASCADE,
    )
    contract_type = models.CharField(
        max_length=500,
        choices=CONTRACT_TYPES
    )
    accepted = models.BooleanField(
        default=False
    )
    fulfilled = models.BooleanField(
        default=False
    )
    # Depreciated
    # expiration = models.DateTimeField()
    deadline_to_accept = models.DateTimeField(
        verbose_name='the time at which the contract is no longer available to be accepted.',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.contract_type} for {self.faction.name}. Payment {self.terms.payment_on_accepted} + {self.terms.payment_on_fulfilled}.'

    @classmethod
    def add(cls, contract_data, faction):
        contract, created = cls.objects.update_or_create(
            contract_id=contract_data['id'],
            defaults={
                'contract_id': contract_data['id'],
                'faction': faction,
                'contract_type': contract_data['type'],
                'accepted': contract_data['accepted'],
                'fulfilled': contract_data['fulfilled'],
                'deadline_to_accept': contract_data['deadlineToAccept']
            }
        )
        terms = Terms.add(contract_data['terms'], contract)
        for delivery_data in contract_data['terms']['deliver']:
            waypoint = Waypoint.objects.get(symbol=delivery_data['destinationSymbol'])
            trade_good = TradeGood.objects.get(symbol=delivery_data['tradeSymbol'])
            Delivery.add(delivery_data=delivery_data, terms=terms, trade_good=trade_good, waypoint=waypoint)
        return contract


class Terms(models.Model):
    contract = models.OneToOneField(
        Contract,
        on_delete=models.CASCADE,
        related_name='terms',
        primary_key=True
    )
    deadline = models.DateTimeField()
    payment_on_accepted = models.IntegerField(
        verbose_name='the amount of credits received up front for accepting the contract.'
    )
    payment_on_fulfilled = models.IntegerField(
        verbose_name='the amount of credits received when the contract is fulfilled.'
    )

    @classmethod
    def add(cls, terms_data, contract):
        terms, created = cls.objects.update_or_create(
            contract=contract,
            defaults={
                'deadline': terms_data['deadline'],
                'payment_on_accepted': terms_data['payment']['onAccepted'],
                'payment_on_fulfilled': terms_data['payment']['onFulfilled']
            }
        )
        return terms


class Delivery(models.Model):
    terms = models.ForeignKey(
        Terms,
        on_delete=models.CASCADE,
        related_name='deliveries'
    )
    trade_good = models.ForeignKey(
        'systems.TradeGood',
        on_delete=models.CASCADE,
    )
    destination = models.ForeignKey(
        'systems.Waypoint',
        on_delete=models.CASCADE,
    )
    units_required = models.IntegerField(
        verbose_name='the number of units that need to be delivered on this contract.'
    )
    units_fulfilled = models.IntegerField(
        verbose_name='the number of units fulfilled on this contract.'
    )

    @classmethod
    def add(cls, delivery_data, terms, trade_good, waypoint):
        delivery, created = cls.objects.update_or_create(
            terms=terms,
            defaults={
                'terms': terms,
                'trade_good': trade_good,
                'destination': waypoint,
                'units_required': delivery_data['unitsRequired'],
                'units_fulfilled': delivery_data['unitsFulfilled']
            }
        )
        return delivery
