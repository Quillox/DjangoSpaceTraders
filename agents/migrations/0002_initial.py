# Generated by Django 4.2.6 on 2023-11-04 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('systems', '0001_initial'),
        ('agents', '0001_initial'),
        ('factions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='headquarters',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent_headquarters', to='systems.waypoint'),
        ),
        migrations.AddField(
            model_name='agent',
            name='starting_faction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='factions.faction'),
        ),
    ]