# Generated by Django 4.2.6 on 2023-11-05 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('symbol', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('credit', models.BigIntegerField(help_text='The number of credits the agent has available. Credits can be negative if funds have been overdrawn.')),
                ('ship_count', models.IntegerField(blank=True, null=True)),
                ('account_id', models.CharField(blank=True, max_length=500, null=True, unique=True)),
            ],
        ),
    ]
