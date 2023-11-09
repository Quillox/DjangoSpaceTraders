# Generated by Django 4.2.6 on 2023-11-09 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0007_remove_shipyardtransaction_ship_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipyardshiplink',
            name='shipyard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ships_for_sale', to='fleet.shipyard'),
        ),
    ]