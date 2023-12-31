# Generated by Django 4.2.6 on 2023-11-09 16:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('systems', '0001_initial'),
        ('agents', '0002_initial'),
        ('factions', '0002_initial'),
        ('fleet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Engine',
            fields=[
                ('tradegood_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='systems.tradegood')),
                ('power', models.IntegerField(blank=True, null=True, verbose_name='the amount of power required from the reactor.')),
                ('crew', models.IntegerField(blank=True, null=True, verbose_name='the amount of crew required for operation.')),
                ('slots', models.IntegerField(blank=True, null=True, verbose_name='the number of module slots required for installation.')),
                ('condition', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='condition is a range of 0 to 100 where 0 is completely worn out and 100 is brand new.')),
                ('speed', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='The speed stat of this engine. The higher the speed, the faster a ship can travel from one point to another. Reduces the time of arrival when navigating the ship.')),
            ],
            options={
                'abstract': False,
            },
            bases=('systems.tradegood',),
        ),
        migrations.CreateModel(
            name='Fleet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('tradegood_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='systems.tradegood')),
                ('power', models.IntegerField(blank=True, null=True, verbose_name='the amount of power required from the reactor.')),
                ('crew', models.IntegerField(blank=True, null=True, verbose_name='the amount of crew required for operation.')),
                ('slots', models.IntegerField(blank=True, null=True, verbose_name='the number of module slots required for installation.')),
                ('condition', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Condition is a range of 0 to 100 where 0 is completely worn out and 100 is brand new.')),
                ('module_slots', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='the amount of slots that can be dedicated to modules installed in the ship. Each installed module take up a number of slots, and once there are no more slots, no new modules can be installed.')),
                ('mounting_points', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='the amount of slots that can be dedicated to mounts installed in the ship. Each installed mount takes up a number of points, and once there are no more points remaining, no new mounts can be installed.')),
                ('fuel_capacity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='the maximum amount of fuel that can be stored in this ship. When refuelling, the ship will be refuelled to this amount.')),
            ],
            options={
                'abstract': False,
            },
            bases=('systems.tradegood',),
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('tradegood_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='systems.tradegood')),
                ('power', models.IntegerField(blank=True, null=True, verbose_name='the amount of power required from the reactor.')),
                ('crew', models.IntegerField(blank=True, null=True, verbose_name='the amount of crew required for operation.')),
                ('slots', models.IntegerField(blank=True, null=True, verbose_name='the number of module slots required for installation.')),
                ('capacity', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='modules that provide capacity, such as cargo hold or crew quarters will show this value to denote how much of a bonus the module grants.')),
                ('sensor_range', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='modules that have a range will such as a sensor array show this value to denote how far can the module reach with its capabilities.')),
            ],
            options={
                'abstract': False,
            },
            bases=('systems.tradegood',),
        ),
        migrations.CreateModel(
            name='Mount',
            fields=[
                ('tradegood_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='systems.tradegood')),
                ('power', models.IntegerField(blank=True, null=True, verbose_name='the amount of power required from the reactor.')),
                ('crew', models.IntegerField(blank=True, null=True, verbose_name='the amount of crew required for operation.')),
                ('slots', models.IntegerField(blank=True, null=True, verbose_name='the number of module slots required for installation.')),
                ('strength', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name="mounts that have this value, such as mining lasers, denote how powerful this mount's capabilities are.")),
            ],
            options={
                'abstract': False,
            },
            bases=('systems.tradegood',),
        ),
        migrations.CreateModel(
            name='Reactor',
            fields=[
                ('tradegood_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='systems.tradegood')),
                ('power', models.IntegerField(blank=True, null=True, verbose_name='the amount of power required from the reactor.')),
                ('crew', models.IntegerField(blank=True, null=True, verbose_name='the amount of crew required for operation.')),
                ('slots', models.IntegerField(blank=True, null=True, verbose_name='the number of module slots required for installation.')),
                ('condition', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='condition is a range of 0 to 100 where 0 is completely worn out and 100 is brand new.')),
                ('power_output', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name="the amount of power provided by this reactor. The more power a reactor provides to the ship, the lower the cooldown it gets when using a module or mount that taxes the ship's power.")),
            ],
            options={
                'abstract': False,
            },
            bases=('systems.tradegood',),
        ),
        migrations.CreateModel(
            name='Ship',
            fields=[
                ('symbol', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('cargo_capacity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='the max number of items that can be stored in the cargo hold.')),
                ('cargo_units', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='the number of items currently stored in the cargo hold.')),
                ('fuel_current', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name="the current amount of fuel in the ship's tanks.")),
                ('fuel_capacity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agents.agent')),
                ('engine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.engine')),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.frame')),
            ],
        ),
        migrations.CreateModel(
            name='Shipyard',
            fields=[
                ('waypoint', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='shipyard', serialize=False, to='systems.waypoint')),
                ('modifications_fee', models.IntegerField(verbose_name='the fee to modify a ship at this shipyard. This includes installing or removing modules and mounts on a ship. In the case of mounts, the fee is a flat rate per mount. In the case of modules, the fee is per slot the module occupies.')),
            ],
        ),
        migrations.CreateModel(
            name='ShipyardShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ship_type', models.CharField(choices=[('SHIP_PROBE', 'Ship Probe'), ('SHIP_MINING_DRONE', 'Ship Mining Drone'), ('SHIP_SIPHON_DRONE', 'Ship Siphon Drone'), ('SHIP_INTERCEPTOR', 'Ship Interceptor'), ('SHIP_LIGHT_HAULER', 'Ship Light Hauler'), ('SHIP_COMMAND_FRIGATE', 'Ship Command Frigate'), ('SHIP_EXPLORER', 'Ship Explorer'), ('SHIP_HEAVY_FREIGHTER', 'Ship Heavy Freighter'), ('SHIP_LIGHT_SHUTTLE', 'Ship Light Shuttle'), ('SHIP_ORE_HOUND', 'Ship Ore Hound'), ('SHIP_REFINING_FREIGHTER', 'Ship Refining Freighter'), ('SHIP_SURVEYOR', 'Ship Surveyor')], max_length=500)),
                ('name', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=5000)),
                ('engine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.engine')),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.frame')),
            ],
        ),
        migrations.CreateModel(
            name='ShipCrew',
            fields=[
                ('ship', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='crew', serialize=False, to='fleet.ship')),
                ('current', models.IntegerField(verbose_name='the current number of crew members on the ship.')),
                ('required', models.IntegerField(verbose_name='the minimum number of crew members required to maintain the ship.')),
                ('capacity', models.IntegerField(default=0, verbose_name='the maximum number of crew members the ship can support.')),
                ('rotation', models.CharField(choices=[('STRICT', 'Strict'), ('RELAXED', 'Relaxed')], default='STRICT', max_length=7, verbose_name="the rotation of crew shifts. A stricter shift improves the ship's performance. A more relaxed shift improves the crew's morale.")),
                ('morale', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name="a rough measure of the crew's morale. A higher morale means the crew is happier and more productive. A lower morale means the ship is more prone to accidents.")),
                ('wages', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='the amount of credits per crew member paid per hour. Wages are paid when a ship docks at a civilized waypoint.')),
            ],
        ),
        migrations.CreateModel(
            name='ShipNav',
            fields=[
                ('ship', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='nav', serialize=False, to='fleet.ship')),
                ('status', models.CharField(choices=[('IN_TRANSIT', 'In Transit'), ('IN_ORBIT', 'In Orbit'), ('DOCKED', 'Docked')], max_length=500)),
                ('flight_mode', models.CharField(choices=[('DRIFT', 'Drift'), ('STEALTH', 'Stealth'), ('CRUISE', 'Cruise'), ('BURN', 'Burn')], default='CRUISE', max_length=500)),
                ('current_system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systems.system')),
                ('waypoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systems.waypoint', verbose_name="The waypoint symbol of the ship's current location, or if the ship is in-transit, the waypoint symbol of the ship's destination.")),
            ],
        ),
        migrations.CreateModel(
            name='ShipyardTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='the price of the transaction.')),
                ('timestamp', models.DateTimeField()),
                ('agent_symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agents.agent', verbose_name='the symbol of the agent that made the transaction.')),
                ('ship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.ship', verbose_name='the symbol of the ship that was the subject of the transaction.')),
                ('shipyard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.shipyard', verbose_name='the symbol of the waypoint where the transaction took place.')),
            ],
        ),
        migrations.CreateModel(
            name='ShipyardShipMountLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mount', models.ForeignKey(choices=[('MOUNT_GAS_SIPHON_I', 'Mount Gas Siphon I'), ('MOUNT_GAS_SIPHON_II', 'Mount Gas Siphon II'), ('MOUNT_GAS_SIPHON_III', 'Mount Gas Siphon III'), ('MOUNT_SURVEYOR_I', 'Mount Surveyor I'), ('MOUNT_SURVEYOR_II', 'Mount Surveyor II'), ('MOUNT_SURVEYOR_III', 'Mount Surveyor III'), ('MOUNT_SENSOR_ARRAY_I', 'Mount Sensor Array I'), ('MOUNT_SENSOR_ARRAY_II', 'Mount Sensor Array II'), ('MOUNT_SENSOR_ARRAY_III', 'Mount Sensor Array III'), ('MOUNT_MINING_LASER_I', 'Mount Mining Laser I'), ('MOUNT_MINING_LASER_II', 'Mount Mining Laser II'), ('MOUNT_MINING_LASER_III', 'Mount Mining Laser III'), ('MOUNT_LASER_CANNON_I', 'Mount Laser Cannon I'), ('MOUNT_MISSILE_LAUNCHER_I', 'Mount Missile Launcher I'), ('MOUNT_TURRET_I', 'Mount Turret I')], on_delete=django.db.models.deletion.CASCADE, to='fleet.mount')),
                ('shipyard_ship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.shipyardship')),
            ],
        ),
        migrations.CreateModel(
            name='ShipyardShipModuleLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.ForeignKey(choices=[('MODULE_MINERAL_PROCESSOR_I', 'Module Mineral Processor I'), ('MODULE_CARGO_HOLD_I', 'Module Cargo Hold I'), ('MODULE_CREW_QUARTERS_I', 'Module Crew Quarters I'), ('MODULE_ENVOY_QUARTERS_I', 'Module Envoy Quarters I'), ('MODULE_PASSENGER_CABIN_I', 'Module Passenger Cabin I'), ('MODULE_MICRO_REFINERY_I', 'Module Micro Refinery I'), ('MODULE_ORE_REFINERY_I', 'Module Ore Refinery I'), ('MODULE_FUEL_REFINERY_I', 'Module Fuel Refinery I'), ('MODULE_SCIENCE_LAB_I', 'Module Science Lab I'), ('MODULE_WARP_DRIVE_I', 'Module Warp Drive I'), ('MODULE_WARP_DRIVE_II', 'Module Warp Drive II'), ('MODULE_WARP_DRIVE_III', 'Module Warp Drive III'), ('MODULE_SHIELD_GENERATOR_I', 'Module Shield Generator I'), ('MODULE_SHIELD_GENERATOR_II', 'Module Shield Generator II')], on_delete=django.db.models.deletion.CASCADE, to='fleet.module')),
                ('shipyard_ship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.shipyardship')),
            ],
        ),
        migrations.CreateModel(
            name='ShipyardShipLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_price', models.IntegerField(verbose_name='the price of the ship at this shipyard.')),
                ('supply', models.CharField(choices=[('SCARCE', 'Scarce'), ('LIMITED', 'Limited'), ('MODERATE', 'Moderate'), ('HIGH', 'High'), ('ABUNDANT', 'Abundant')], max_length=500, verbose_name='the supply of the ship at this shipyard.')),
                ('activity', models.CharField(choices=[('WEAK', 'Weak'), ('GROWING', 'Growing'), ('STRONG', 'Strong')], max_length=500, verbose_name='the activity level of a trade good. If the good is an import, this represents how strong consumption is for the good. If the good is an export, this represents how strong the production is for the good.')),
                ('shipyard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.shipyard')),
                ('shipyard_ship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.shipyardship')),
            ],
        ),
        migrations.AddField(
            model_name='shipyardship',
            name='modules',
            field=models.ManyToManyField(related_name='shipyard_ships', through='fleet.ShipyardShipModuleLink', to='fleet.module'),
        ),
        migrations.AddField(
            model_name='shipyardship',
            name='mounts',
            field=models.ManyToManyField(related_name='shipyard_ships', through='fleet.ShipyardShipMountLink', to='fleet.mount'),
        ),
        migrations.AddField(
            model_name='shipyardship',
            name='reactor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.reactor'),
        ),
        migrations.AddField(
            model_name='shipyard',
            name='ships',
            field=models.ManyToManyField(related_name='shipyards', through='fleet.ShipyardShipLink', to='fleet.shipyardship', verbose_name='the list of ship types available for purchase at this shipyard..'),
        ),
        migrations.CreateModel(
            name='ShipMountLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mount', models.ForeignKey(choices=[('MOUNT_GAS_SIPHON_I', 'Mount Gas Siphon I'), ('MOUNT_GAS_SIPHON_II', 'Mount Gas Siphon II'), ('MOUNT_GAS_SIPHON_III', 'Mount Gas Siphon III'), ('MOUNT_SURVEYOR_I', 'Mount Surveyor I'), ('MOUNT_SURVEYOR_II', 'Mount Surveyor II'), ('MOUNT_SURVEYOR_III', 'Mount Surveyor III'), ('MOUNT_SENSOR_ARRAY_I', 'Mount Sensor Array I'), ('MOUNT_SENSOR_ARRAY_II', 'Mount Sensor Array II'), ('MOUNT_SENSOR_ARRAY_III', 'Mount Sensor Array III'), ('MOUNT_MINING_LASER_I', 'Mount Mining Laser I'), ('MOUNT_MINING_LASER_II', 'Mount Mining Laser II'), ('MOUNT_MINING_LASER_III', 'Mount Mining Laser III'), ('MOUNT_LASER_CANNON_I', 'Mount Laser Cannon I'), ('MOUNT_MISSILE_LAUNCHER_I', 'Mount Missile Launcher I'), ('MOUNT_TURRET_I', 'Mount Turret I')], on_delete=django.db.models.deletion.CASCADE, to='fleet.mount')),
                ('ship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.ship')),
            ],
        ),
        migrations.CreateModel(
            name='ShipModuleLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.ForeignKey(choices=[('MODULE_MINERAL_PROCESSOR_I', 'Module Mineral Processor I'), ('MODULE_CARGO_HOLD_I', 'Module Cargo Hold I'), ('MODULE_CREW_QUARTERS_I', 'Module Crew Quarters I'), ('MODULE_ENVOY_QUARTERS_I', 'Module Envoy Quarters I'), ('MODULE_PASSENGER_CABIN_I', 'Module Passenger Cabin I'), ('MODULE_MICRO_REFINERY_I', 'Module Micro Refinery I'), ('MODULE_ORE_REFINERY_I', 'Module Ore Refinery I'), ('MODULE_FUEL_REFINERY_I', 'Module Fuel Refinery I'), ('MODULE_SCIENCE_LAB_I', 'Module Science Lab I'), ('MODULE_WARP_DRIVE_I', 'Module Warp Drive I'), ('MODULE_WARP_DRIVE_II', 'Module Warp Drive II'), ('MODULE_WARP_DRIVE_III', 'Module Warp Drive III'), ('MODULE_SHIELD_GENERATOR_I', 'Module Shield Generator I'), ('MODULE_SHIELD_GENERATOR_II', 'Module Shield Generator II')], on_delete=django.db.models.deletion.CASCADE, to='fleet.module')),
                ('ship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.ship')),
            ],
        ),
        migrations.CreateModel(
            name='ShipCargoInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('units', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('ship_symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.ship')),
                ('trade_good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systems.tradegood')),
            ],
        ),
        migrations.AddField(
            model_name='ship',
            name='modules',
            field=models.ManyToManyField(related_name='ships', through='fleet.ShipModuleLink', to='fleet.module'),
        ),
        migrations.AddField(
            model_name='ship',
            name='mounts',
            field=models.ManyToManyField(related_name='ships', through='fleet.ShipMountLink', to='fleet.mount'),
        ),
        migrations.AddField(
            model_name='ship',
            name='reactor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.reactor'),
        ),
        migrations.CreateModel(
            name='MountDepositLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposits_link', to='fleet.mount')),
                ('trade_good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposited_by_link', to='systems.tradegood')),
            ],
        ),
        migrations.AddField(
            model_name='mount',
            name='deposits',
            field=models.ManyToManyField(choices=[('QUARTZ_SAND', 'Quartz Sand'), ('SILICON_CRYSTALS', 'Silicon Crystals'), ('PRECIOUS_STONES', 'Precious Stones'), ('ICE_WATER', 'Ice Water'), ('AMMONIA_ICE', 'Ammonia Ice'), ('IRON_ORE', 'Iron Ore'), ('COPPER_ORE', 'Copper Ore'), ('SILVER_ORE', 'Silver Ore'), ('ALUMINUM_ORE', 'Aluminum Ore'), ('GOLD_ORE', 'Gold Ore'), ('PLATINUM_ORE', 'Platinum Ore'), ('DIAMONDS', 'Diamonds'), ('URANITE_ORE', 'Uranite Ore'), ('MERITIUM_ORE', 'Meritium Ore')], related_name='mounts', through='fleet.MountDepositLink', to='systems.tradegood'),
        ),
        migrations.CreateModel(
            name='FuelConsumedLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='the amount of fuel consumed by the most recent transit or action.')),
                ('timestamp', models.DateTimeField(verbose_name='the time at which the fuel was consumed.')),
                ('ship_symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.ship')),
            ],
        ),
        migrations.AddField(
            model_name='cooldown',
            name='ship_symbol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.ship'),
        ),
        migrations.AddField(
            model_name='shipyardship',
            name='crew',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.shipcrew'),
        ),
        migrations.CreateModel(
            name='ShipRegistration',
            fields=[
                ('ship', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='registration', serialize=False, to='fleet.ship')),
                ('ship_role', models.CharField(choices=[('FABRICATOR', 'Fabricator'), ('HARVESTER', 'Harvester'), ('HAULER', 'Hauler'), ('INTERCEPTOR', 'Interceptor'), ('EXCAVATOR', 'Excavator'), ('TRANSPORT', 'Transport'), ('REPAIR', 'Repair'), ('SURVEYOR', 'Surveyor'), ('COMMAND', 'Command'), ('CARRIER', 'Carrier'), ('PATROL', 'Patrol'), ('SATELLITE', 'Satellite'), ('EXPLORER', 'Explorer'), ('REFINERY', 'Refinery')], max_length=500)),
                ('faction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='factions.faction')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agents.agent')),
            ],
        ),
        migrations.CreateModel(
            name='ShipNavRoute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField(verbose_name="the date time of the ship's arrival. If the ship is in-transit, this is the expected time of arrival.")),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nav_destination', to='systems.waypoint')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nav_origin', to='systems.waypoint')),
                ('ship_nav', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='route', to='fleet.shipnav')),
            ],
        ),
    ]
