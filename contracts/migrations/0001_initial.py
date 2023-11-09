# Generated by Django 4.2.6 on 2023-11-09 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('contract_id', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('contract_type', models.CharField(choices=[('PROCUREMENT', 'Procurement'), ('TRANSPORT', 'Transport'), ('SHUTTLE', 'Shuttle')], max_length=500)),
                ('accepted', models.BooleanField(default=False)),
                ('fulfilled', models.BooleanField(default=False)),
                ('deadline_to_accept', models.DateTimeField(blank=True, null=True, verbose_name='the time at which the contract is no longer available to be accepted.')),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('units_required', models.IntegerField(verbose_name='the number of units that need to be delivered on this contract.')),
                ('units_fulfilled', models.IntegerField(verbose_name='the number of units fulfilled on this contract.')),
            ],
        ),
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('contract', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='terms', serialize=False, to='contracts.contract')),
                ('deadline', models.DateTimeField()),
                ('payment_on_accepted', models.IntegerField(verbose_name='the amount of credits received up front for accepting the contract.')),
                ('payment_on_fulfilled', models.IntegerField(verbose_name='the amount of credits received when the contract is fulfilled.')),
            ],
        ),
    ]
