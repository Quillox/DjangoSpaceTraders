# Generated by Django 4.2.6 on 2023-11-12 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systems', '0004_alter_markettradegoodlink_activity'),
        ('fleet', '0008_alter_shipyardshiplink_shipyard'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cooldown',
            old_name='ship_symbol',
            new_name='ship',
        ),
        migrations.AlterField(
            model_name='mount',
            name='deposits',
            field=models.ManyToManyField(choices=[('QUARTZ_SAND', 'Quartz Sand'), ('SILICON_CRYSTALS', 'Silicon Crystals'), ('PRECIOUS_STONES', 'Precious Stones'), ('ICE_WATER', 'Ice Water'), ('AMMONIA_ICE', 'Ammonia Ice'), ('IRON_ORE', 'Iron Ore'), ('COPPER_ORE', 'Copper Ore'), ('SILVER_ORE', 'Silver Ore'), ('ALUMINUM_ORE', 'Aluminum Ore'), ('GOLD_ORE', 'Gold Ore'), ('PLATINUM_ORE', 'Platinum Ore'), ('DIAMONDS', 'Diamonds'), ('URANITE_ORE', 'Uranite Ore'), ('MERITIUM_ORE', 'Meritium Ore')], related_name='mounts', through='fleet.MountDepositLink', to='systems.tradegood', verbose_name='mounts that have this value denote what goods can be produced from using the mount.'),
        ),
    ]