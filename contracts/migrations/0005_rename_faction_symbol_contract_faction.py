# Generated by Django 4.2.6 on 2023-11-02 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0004_rename_trade_good_symbol_delivery_trade_good'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract',
            old_name='faction_symbol',
            new_name='faction',
        ),
    ]
