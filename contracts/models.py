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
    faction_symbol = models.ForeignKey(
        'factions.Faction',
        on_delete=models.CASCADE,
    )
    contract_type = models.CharField(
        max_length=500,
        choices=CONTRACT_TYPES
    )
    # TODO implement this
    terms = models.OneToOneField(
        'Terms',
        on_delete=models.CASCADE,
        related_name='contract'
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

    @classmethod
    def add(cls, contract_data, faction, waypoint, trade_good):
        contract, created = cls.objects.update_or_create(
            contract_id=contract_data['id'],
            faction_symbol=faction,
            contract_type=contract_data['type'],
            accepted=contract_data['accepted'],
            fulfilled=contract_data['fulfilled'],
            deadline_to_accept=contract_data['deadlineToAccept']
        )
        terms = Terms.add(contract_data['terms'], contract)
        Delivery.add(contract_data['terms']['deliver'], trade_good, waypoint, terms)


class Terms(models.Model):
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name='terms'
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
            deadline=terms_data['deadline'],
            payment_on_accepted=terms_data['payment']['onAccepted'],
            payment_on_fulfilled=terms_data['payment']['onFulfilled']
        )
        return terms


class Delivery(models.Model):
    terms = models.ForeignKey(
        Terms,
        on_delete=models.CASCADE,
    )
    trade_good_symbol = models.ForeignKey(
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
            trade_good_symbol=trade_good,
            destination=waypoint,
            units_required=delivery_data['unitsRequired'],
            units_fulfilled=delivery_data['unitsFulfilled']
        )
        return delivery
