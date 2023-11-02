from typing import List
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from systems.models import TradeGood, MARKET_SUPPLY, MARKET_ACTIVITY


SHIP_ROLE = [
    ('FABRICATOR', 'Fabricator'),
    ('HARVESTER', 'Harvester'),
    ('HAULER', 'Hauler'),
    ('INTERCEPTOR', 'Interceptor'),
    ('EXCAVATOR', 'Excavator'),
    ('TRANSPORT', 'Transport'),
    ('REPAIR', 'Repair'),
    ('SURVEYOR', 'Surveyor'),
    ('COMMAND', 'Command'),
    ('CARRIER', 'Carrier'),
    ('PATROL', 'Patrol'),
    ('SATELLITE', 'Satellite'),
    ('EXPLORER', 'Explorer'),
    ('REFINERY', 'Refinery')
]

SHIP_NAV_STATUS = [
    ('IN_TRANSIT', 'In Transit'),
    ('IN_ORBIT', 'In Orbit'),
    ('DOCKED', 'Docked')
]

SHIP_FLIGHT_MODE = [
    ('DRIFT', 'Drift'),
    ('STEALTH', 'Stealth'),
    ('CRUISE', 'Cruise'),
    ('BURN', 'Burn')
]

SHIP_CREW_ROTATION = [
    ('STRICT', 'Strict'),
    ('RELAXED', 'Relaxed')
]

SHIP_FRAME_SYMBOL = [
    ('FRAME_PROBE', 'Frame Probe'),
    ('FRAME_DRONE', 'Frame Drone'),
    ('FRAME_INTERCEPTOR', 'Frame Interceptor'),
    ('FRAME_RACER', 'Frame Racer'),
    ('FRAME_FIGHTER', 'Frame Fighter'),
    ('FRAME_FRIGATE', 'Frame Frigate'),
    ('FRAME_SHUTTLE', 'Frame Shuttle'),
    ('FRAME_EXPLORER', 'Frame Explorer'),
    ('FRAME_MINER', 'Frame Miner'),
    ('FRAME_LIGHT_FREIGHTER', 'Frame Light Freighter'),
    ('FRAME_HEAVY_FREIGHTER', 'Frame Heavy Freighter'),
    ('FRAME_TRANSPORT', 'Frame Transport'),
    ('FRAME_DESTROYER', 'Frame Destroyer'),
    ('FRAME_CRUISER', 'Frame Cruiser'),
    ('FRAME_CARRIER', 'Frame Carrier')
]

SHIP_REACTOR_SYMBOL = [
    ('REACTOR_SOLAR_I', 'Reactor Solar I'),
    ('REACTOR_FUSION_I', 'Reactor Fusion I'),
    ('REACTOR_FISSION_I', 'Reactor Fission I'),
    ('REACTOR_CHEMICAL_I', 'Reactor Chemical I'),
    ('REACTOR_ANTIMATTER_I', 'Reactor Antimatter I')
]

SHIP_ENGINE_SYMBOL = [
    ('ENGINE_IMPULSE_DRIVE_I', 'Engine Impulse Drive I'),
    ('ENGINE_ION_DRIVE_I', 'Engine Ion Drive I'),
    ('ENGINE_ION_DRIVE_II', 'Engine Ion Drive II'),
    ('ENGINE_HYPER_DRIVE_I', 'Engine Hyper Drive I')
]

SHIP_MODULE_SYMBOL = [
    ('MODULE_MINERAL_PROCESSOR_I', 'Module Mineral Processor I'),
    ('MODULE_CARGO_HOLD_I', 'Module Cargo Hold I'),
    ('MODULE_CREW_QUARTERS_I', 'Module Crew Quarters I'),
    ('MODULE_ENVOY_QUARTERS_I', 'Module Envoy Quarters I'),
    ('MODULE_PASSENGER_CABIN_I', 'Module Passenger Cabin I'),
    ('MODULE_MICRO_REFINERY_I', 'Module Micro Refinery I'),
    ('MODULE_ORE_REFINERY_I', 'Module Ore Refinery I'),
    ('MODULE_FUEL_REFINERY_I', 'Module Fuel Refinery I'),
    ('MODULE_SCIENCE_LAB_I', 'Module Science Lab I'),
    ('MODULE_WARP_DRIVE_I', 'Module Warp Drive I'),
    ('MODULE_WARP_DRIVE_II', 'Module Warp Drive II'),
    ('MODULE_WARP_DRIVE_III', 'Module Warp Drive III'),
    ('MODULE_SHIELD_GENERATOR_I', 'Module Shield Generator I'),
    ('MODULE_SHIELD_GENERATOR_II', 'Module Shield Generator II')
]

SHIP_MOUNT_SYMBOL = [
    ('MOUNT_GAS_SIPHON_I', 'Mount Gas Siphon I'),
    ('MOUNT_GAS_SIPHON_II', 'Mount Gas Siphon II'),
    ('MOUNT_GAS_SIPHON_III', 'Mount Gas Siphon III'),
    ('MOUNT_SURVEYOR_I', 'Mount Surveyor I'),
    ('MOUNT_SURVEYOR_II', 'Mount Surveyor II'),
    ('MOUNT_SURVEYOR_III', 'Mount Surveyor III'),
    ('MOUNT_SENSOR_ARRAY_I', 'Mount Sensor Array I'),
    ('MOUNT_SENSOR_ARRAY_II', 'Mount Sensor Array II'),
    ('MOUNT_SENSOR_ARRAY_III', 'Mount Sensor Array III'),
    ('MOUNT_MINING_LASER_I', 'Mount Mining Laser I'),
    ('MOUNT_MINING_LASER_II', 'Mount Mining Laser II'),
    ('MOUNT_MINING_LASER_III', 'Mount Mining Laser III'),
    ('MOUNT_LASER_CANNON_I', 'Mount Laser Cannon I'),
    ('MOUNT_MISSILE_LAUNCHER_I', 'Mount Missile Launcher I'),
    ('MOUNT_TURRET_I', 'Mount Turret I')
]

SHIP_COMPONENT_SYMBOL = [
    *SHIP_FRAME_SYMBOL,
    *SHIP_REACTOR_SYMBOL,
    *SHIP_ENGINE_SYMBOL,
    *SHIP_MODULE_SYMBOL,
    *SHIP_MOUNT_SYMBOL
]

SHIP_MOUNT_DEPOSIT_SYMBOL = [
    ('QUARTZ_SAND', 'Quartz Sand'),
    ('SILICON_CRYSTALS', 'Silicon Crystals'),
    ('PRECIOUS_STONES', 'Precious Stones'),
    ('ICE_WATER', 'Ice Water'),
    ('AMMONIA_ICE', 'Ammonia Ice'),
    ('IRON_ORE', 'Iron Ore'),
    ('COPPER_ORE', 'Copper Ore'),
    ('SILVER_ORE', 'Silver Ore'),
    ('ALUMINUM_ORE', 'Aluminum Ore'),
    ('GOLD_ORE', 'Gold Ore'),
    ('PLATINUM_ORE', 'Platinum Ore'),
    ('DIAMONDS', 'Diamonds'),
    ('URANITE_ORE', 'Uranite Ore'),
    ('MERITIUM_ORE', 'Meritium Ore')
]

SHIP_TYPE = [
    ('SHIP_PROBE', 'Ship Probe'),
    ('SHIP_MINING_DRONE', 'Ship Mining Drone'),
    ('SHIP_SIPHON_DRONE', 'Ship Siphon Drone'),
    ('SHIP_INTERCEPTOR', 'Ship Interceptor'),
    ('SHIP_LIGHT_HAULER', 'Ship Light Hauler'),
    ('SHIP_COMMAND_FRIGATE', 'Ship Command Frigate'),
    ('SHIP_EXPLORER', 'Ship Explorer'),
    ('SHIP_HEAVY_FREIGHTER', 'Ship Heavy Freighter'),
    ('SHIP_LIGHT_SHUTTLE', 'Ship Light Shuttle'),
    ('SHIP_ORE_HOUND', 'Ship Ore Hound'),
    ('SHIP_REFINING_FREIGHTER', 'Ship Refining Freighter'),
    ('SHIP_SURVEYOR', 'Ship Surveyor')
]


# TODO ctrl+F waypoint and system and replace with ForeignKey to Waypoint and System

class Fleet(models.Model):
    pass

class ShipRegistration(models.Model):
    ship = models.OneToOneField(
        'fleet.Ship',
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='registration'
    )
    name = models.ForeignKey(
        'agents.Agent',
        on_delete=models.CASCADE,
    )
    faction = models.ForeignKey(
        'factions.Faction',
        on_delete=models.CASCADE,
    )
    ship_role = models.CharField(
        max_length=500,
        choices=SHIP_ROLE
    )

    @classmethod
    def add(cls, ship_registration_data, ship, agent, faction):
        registration, created = cls.objects.update_or_create(
            ship=ship,
            name=agent,
            defaults={
                'ship': ship,
                'name': agent,
                'faction': faction,
                'ship_role': ship_registration_data['role']
            }
        )
        return registration


class ShipNav(models.Model):
    current_system = models.ForeignKey(
        'systems.System',
        on_delete=models.CASCADE,
    )
    waypoint = models.ForeignKey(
        'systems.Waypoint',
        on_delete=models.CASCADE,
        verbose_name="The waypoint symbol of the ship's current location, or if the ship is in-transit, the waypoint symbol of the ship's destination."
    )
    route = models.ForeignKey(
        'ShipNavRoute',
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=500,
        choices=SHIP_NAV_STATUS
    )
    flight_mode = models.CharField(
        max_length=500,
        choices=SHIP_FLIGHT_MODE,
        default='CRUISE'
    )

    @classmethod
    def add(cls, ship_nav_data, system, waypoint, route):
        ship_nav, created = cls.objects.update_or_create(
            current_system=system,
            waypoint=waypoint,
            route=route,
            status=ship_nav_data['status'],
            flight_mode=ship_nav_data['flightMode'],
            defaults={
                'current_system': system,
                'waypoint': waypoint,
                'route': route,
                'status': ship_nav_data['status'],
                'flight_mode': ship_nav_data['flightMode']
            }
        )
        return ship_nav


class ShipNavRoute(models.Model):
    destination = models.ForeignKey(
        'systems.Waypoint',
        on_delete=models.CASCADE,
        related_name='nav_destination'
    )
    # departure_waypoint = models.ForeignKey(
    #     'systems.Waypoint',
    #     on_delete=models.CASCADE,
    #     verbose_name='Depreciated, use origin',
    #     related_name='nav_departure'
    # )
    origin = models.ForeignKey(
        'systems.Waypoint',
        on_delete=models.CASCADE,
        related_name='nav_origin'
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField(
        verbose_name="the date time of the ship's arrival. If the ship is in-transit, this is the expected time of arrival."
    )

    @classmethod
    def add(cls, ship_nav_route_data, destination, origin):
        ship_nav_route, created = cls.objects.update_or_create(
            destination=destination,
            origin=origin,
            departure_time=ship_nav_route_data['departureTime'],
            arrival_time=ship_nav_route_data['arrival'],
            defaults={
                'destination': destination,
                'origin': origin,
                'departure_time': ship_nav_route_data['departureTime'],
                'arrival_time': ship_nav_route_data['arrival']
            }
        )
        return ship_nav_route


class ShipCrew(models.Model):
    # TODO add OneToOneField to Ship
    current = models.IntegerField(
        verbose_name='the current number of crew members on the ship.'
    )
    required = models.IntegerField(
        verbose_name='the minimum number of crew members required to maintain the ship.'
    )
    capacity = models.IntegerField(
        verbose_name='the maximum number of crew members the ship can support.',
        default=0
    )
    rotation = models.CharField(
        max_length=7,
        choices=SHIP_CREW_ROTATION,
        default='STRICT',
        verbose_name='the rotation of crew shifts. A stricter shift improves the ship\'s performance. A more relaxed shift improves the crew\'s morale.'
    )
    morale = models.IntegerField(
        verbose_name='a rough measure of the crew\'s morale. A higher morale means the crew is happier and more productive. A lower morale means the ship is more prone to accidents.',
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    wages = models.IntegerField(
        verbose_name='the amount of credits per crew member paid per hour. Wages are paid when a ship docks at a civilized waypoint.',
        validators=[MinValueValidator(0)]
    )

    @classmethod
    def add(cls, ship_crew_data):
        ship_crew, created = cls.objects.update_or_create(
            current=ship_crew_data['current'],
            required=ship_crew_data['required'],
            capacity=ship_crew_data['capacity'],
            rotation=ship_crew_data['rotation'],
            morale=ship_crew_data['morale'],
            wages=ship_crew_data['wages'],
            defaults={
                'current': ship_crew_data['current'],
                'required': ship_crew_data['required'],
                'capacity': ship_crew_data['capacity'],
                'rotation': ship_crew_data['rotation'],
                'morale': ship_crew_data['morale'],
                'wages': ship_crew_data['wages']
            }
        )
        return ship_crew


class ShipComponent(TradeGood):
    power = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="the amount of power required from the reactor."
    )
    crew = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="the amount of crew required for operation."
    )
    slots = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="the number of module slots required for installation."
    )

    class Meta:
        abstract = True


class Frame(ShipComponent):
    condition = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Condition is a range of 0 to 100 where 0 is completely worn out and 100 is brand new."
    )
    module_slots = models.IntegerField(
        verbose_name='the amount of slots that can be dedicated to modules installed in the ship. Each installed module take up a number of slots, and once there are no more slots, no new modules can be installed.',
        validators=[MinValueValidator(0)]
    )
    mounting_points = models.IntegerField(
        verbose_name='the amount of slots that can be dedicated to mounts installed in the ship. Each installed mount takes up a number of points, and once there are no more points remaining, no new mounts can be installed.',
        validators=[MinValueValidator(0)]
    )
    fuel_capacity = models.IntegerField(
        verbose_name='the maximum amount of fuel that can be stored in this ship. When refuelling, the ship will be refuelled to this amount.',
        validators=[MinValueValidator(0)]
    )

    @classmethod
    def add(cls, frame_data):
        frame, created = cls.objects.update_or_create(
            symbol=frame_data['symbol'],
            defaults={
                'symbol': frame_data['symbol'],
                'name': frame_data['name'],
                'description': frame_data['description'],
                'condition': frame_data['condition'],
                'module_slots': frame_data['moduleSlots'],
                'mounting_points': frame_data['mountingPoints'],
                'fuel_capacity': frame_data['fuelCapacity'],
                'power': frame_data['requirements'].get('power'),
                'crew': frame_data['requirements'].get('crew'),
                'slots': frame_data['requirements'].get('slots')
            }
        )
        return frame


class Reactor(ShipComponent):
    condition = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='condition is a range of 0 to 100 where 0 is completely worn out and 100 is brand new.'
    )
    power_output = models.IntegerField(
        verbose_name='the amount of power provided by this reactor. The more power a reactor provides to the ship, the lower the cooldown it gets when using a module or mount that taxes the ship\'s power.',
        validators=[MinValueValidator(1)]
    )

    @classmethod
    def add(cls, reactor_data):
        reactor, created = cls.objects.update_or_create(
            symbol=reactor_data['symbol'],
            defaults={
                'symbol': reactor_data['symbol'],
                'name': reactor_data['name'],
                'description': reactor_data['description'],
                'condition': reactor_data['condition'],
                'power_output': reactor_data['powerOutput'],
                'power': reactor_data['requirements'].get('power'),
                'crew': reactor_data['requirements'].get('crew'),
                'slots': reactor_data['requirements'].get('slots')
            }
        )
        return reactor


class Engine(ShipComponent):
    condition = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='condition is a range of 0 to 100 where 0 is completely worn out and 100 is brand new.'
    )
    speed = models.IntegerField(
        verbose_name='The speed stat of this engine. The higher the speed, the faster a ship can travel from one point to another. Reduces the time of arrival when navigating the ship.',
        validators=[MinValueValidator(1)]
    )

    @classmethod
    def add(cls, engine_data):
        engine, created = cls.objects.update_or_create(
            symbol=engine_data['symbol'],
            defaults={
                'symbol': engine_data['symbol'],
                'name': engine_data['name'],
                'description': engine_data['description'],
                'condition': engine_data['condition'],
                'speed': engine_data['speed'],
                'power': engine_data['requirements'].get('power'),
                'crew': engine_data['requirements'].get('crew'),
                'slots': engine_data['requirements'].get('slots')
            }
        )
        return engine

class Module(ShipComponent):
    capacity = models.IntegerField(
        verbose_name='modules that provide capacity, such as cargo hold or crew quarters will show this value to denote how much of a bonus the module grants.',
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )
    sensor_range = models.IntegerField(
        verbose_name='modules that have a range will such as a sensor array show this value to denote how far can the module reach with its capabilities.',
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )

    @classmethod
    def add(cls, module_data):
        module, created = cls.objects.update_or_create(
            symbol=module_data['symbol'],
            defaults={
                'symbol': module_data['symbol'],
                'name': module_data['name'],
                'description': module_data['description'],
                'capacity': module_data.get('capacity'),
                'sensor_range': module_data.get('sensorRange'),
                'power': module_data['requirements'].get('power'),
                'crew': module_data['requirements'].get('crew'),
                'slots': module_data['requirements'].get('slots')
            }
        )
        return module


class Mount(ShipComponent):
    strength = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="mounts that have this value, such as mining lasers, denote how powerful this mount's capabilities are.",
        validators=[MinValueValidator(0)]
    )
    deposits = models.ManyToManyField(
         'systems.TradeGood',
        through='MountDepositLink',
        related_name='mounts',
        choices=SHIP_MOUNT_DEPOSIT_SYMBOL
    )

    @classmethod
    def add(cls, mount_data, deposits: list):
        mount, created = cls.objects.update_or_create(
            symbol=mount_data['symbol'],
            defaults={
                'symbol': mount_data['symbol'],
                'name': mount_data['name'],
                'description': mount_data['description'],
                'strength': mount_data.get('strength'),
                'power': mount_data['requirements'].get('power'),
                'crew': mount_data['requirements'].get('crew'),
                'slots': mount_data['requirements'].get('slots')
            }
        )

        for deposit in deposits:
            MountDepositLink.add(mount, deposit)

        return mount


class MountDepositLink(models.Model):
    mount = models.ForeignKey(
        Mount,
        on_delete=models.CASCADE,
        related_name='deposits_link'
    )
    trade_good = models.ForeignKey(
         'systems.TradeGood',
        on_delete=models.CASCADE,
        related_name='deposited_by_link'
    )

    @classmethod
    def add(cls, mount, deposit):
        mount_deposit_link, created = cls.objects.update_or_create(
            mount=mount,
            trade_good=deposit,
            defaults={
                'mount': mount,
                'trade_good': deposit
            }
        )
        return mount_deposit_link


class Ship(models.Model):
    agent = models.ForeignKey(
         'agents.Agent',
        on_delete=models.CASCADE
    )
    # [AGENT_SYMBOL]-[HEX_ID]
    symbol = models.CharField(
        primary_key=True,
        max_length=500,
    )
    nav = models.OneToOneField(
        ShipNav,
        on_delete=models.CASCADE,
    )
    crew = models.OneToOneField(
        ShipCrew,
        on_delete=models.CASCADE,
    )
    frame = models.ForeignKey(
        Frame,
        on_delete=models.CASCADE,
    )
    reactor = models.ForeignKey(
        Reactor,
        on_delete=models.CASCADE,
    )
    engine = models.ForeignKey(
        Engine,
        on_delete=models.CASCADE,
    )
    modules = models.ManyToManyField(
        Module,
        through='ShipModuleLink',
        related_name='ships'
    )
    mounts = models.ManyToManyField(
        Mount,
        through='ShipMountLink',
        related_name='ships'
    )
    cargo_capacity = models.IntegerField(
        verbose_name="the max number of items that can be stored in the cargo hold.",
        validators=[MinValueValidator(0)]
    )
    cargo_units = models.IntegerField(
        verbose_name="the number of items currently stored in the cargo hold.",
        validators=[MinValueValidator(0)]
    )
    fuel_current = models.IntegerField(
        verbose_name="the current amount of fuel in the ship's tanks.",
        validators=[MinValueValidator(0)]
    )
    fuel_capacity = models.IntegerField(
        validators=[MinValueValidator(0)]
    )

    @classmethod
    def add(cls, ship_data, agent, faction, nav, crew, frame, reactor, engine, modules: List[Module], mounts: List[Mount]):
        ship, created = cls.objects.update_or_create(
            agent=agent,
            symbol=ship_data['symbol'],
            defaults={
                'agent': agent,
                'symbol': ship_data['symbol'],
                'nav': nav,
                'crew': crew,
                'frame': frame,
                'reactor': reactor,
                'engine': engine,
                'cargo_capacity': ship_data['cargo']['capacity'],
                'cargo_units': ship_data['cargo']['units'],
                'fuel_current': ship_data['fuel']['current'],
                'fuel_capacity': ship_data['fuel']['capacity']
            }
        )

        ShipRegistration.add(
            ship_data['registration'],
            ship,
            agent,
            faction,
        )

        # TODO look into `bulk_create`
        for module in modules:
            ShipModuleLink.add(ship, module)

        for mount in mounts:
            ShipMountLink.add(ship, mount)

        return ship


class Cooldown(models.Model):
    ship_symbol = models.ForeignKey(
        Ship,
        on_delete=models.CASCADE,
    )
    total_seconds = models.IntegerField(
        verbose_name='the total duration of the cooldown in seconds.',
        validators=[MinValueValidator(0)]
    )
    remaining_seconds = models.IntegerField(
        verbose_name='the remaining duration of the cooldown in seconds',
        validators=[MinValueValidator(0)]
    )
    expiration = models.DateTimeField(
        verbose_name='the date and time when the cooldown expires in ISO 8601 format.',
        blank=True,
        null=True
    )

    @classmethod
    def add(cls, cooldown_data, ship):
        cooldown, created = cls.objects.update_or_create(
            ship_symbol=ship,
            defaults={
                'ship_symbol': ship,
                'total_seconds': cooldown_data['totalSeconds'],
                'remaining_seconds': cooldown_data['remainingSeconds'],
                'expiration': cooldown_data['expiration']
            }
        )
        return cooldown

class ShipCargoInventory(models.Model):
    ship_symbol = models.ForeignKey(
        Ship,
        on_delete=models.CASCADE,
    )
    trade_good = models.ForeignKey(
         TradeGood,
        on_delete=models.CASCADE,
    )
    units = models.IntegerField(
        validators=[MinValueValidator(1)]
    )

    @classmethod
    def add(cls, inventory_data, ship):
        ship_cargo_inventory = []
        for trade_good_data in inventory_data:
            ship_cargo_inventory.append(
                cls.objects.update_or_create(
                    ship_symbol=ship,
                    trade_good=TradeGood.add(trade_good_data),
                    defaults={
                        'ship_symbol': ship,
                        'trade_good': TradeGood.add(trade_good_data),
                        'units': trade_good_data['units']
                    }
                )
            )
        return ship_cargo_inventory


class FuelConsumedLog(models.Model):
    ship_symbol = models.ForeignKey(
        Ship,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        verbose_name="the amount of fuel consumed by the most recent transit or action.",
        validators=[MinValueValidator(0)]
    )
    timestamp = models.DateTimeField(
        verbose_name='the time at which the fuel was consumed.'
    )

    @classmethod
    def add(cls, fuel_consumed_log_data, ship):
        fuel_consumed_log, created = cls.objects.update_or_create(
            ship_symbol=ship,
            defaults={
                'ship_symbol': ship,
                'amount': fuel_consumed_log_data['amount'],
                'timestamp': fuel_consumed_log_data['timestamp']
            }
        )
        return fuel_consumed_log


class ShipModuleLink(models.Model):
    ship = models.ForeignKey(
        Ship,
        on_delete=models.CASCADE,
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        choices=SHIP_MODULE_SYMBOL
    )

    @classmethod
    def add(cls, ship, module):
        ship_module_link, created = cls.objects.update_or_create(
            ship=ship,
            module=module,
            defaults={
                'ship': ship,
                'module': module
            }
        )
        return ship_module_link


class ShipMountLink(models.Model):
    ship = models.ForeignKey(
        Ship,
        on_delete=models.CASCADE,
    )
    mount = models.ForeignKey(
        Mount,
        on_delete=models.CASCADE,
        choices=SHIP_MOUNT_SYMBOL
    )

    @classmethod
    def add(cls, ship, mount):
        ship_mount_link, created = cls.objects.update_or_create(
            ship=ship,
            mount=mount,
            defaults={
                'ship': ship,
                'mount': mount
            }
        )
        return ship_mount_link


# TODO make an abstract base class for ShipyardShip and Ship
# TODO Maybe move the shipyard to the systems app
class ShipyardShip(models.Model):
    ship_type = models.CharField(
        max_length=500,
        choices=SHIP_TYPE
    )
    name = models.CharField(
        max_length=500
    )
    description = models.CharField(
        max_length=5000
    )
    frame = models.ForeignKey(
        Frame,
        on_delete=models.CASCADE,
    )
    reactor = models.ForeignKey(
        Reactor,
        on_delete=models.CASCADE,
    )
    engine = models.ForeignKey(
        Engine,
        on_delete=models.CASCADE,
    )
    modules = models.ManyToManyField(
        Module,
        through='ShipyardShipModuleLink',
        related_name='shipyard_ships'
    )
    mounts = models.ManyToManyField(
        Mount,
        through='ShipyardShipMountLink',
        related_name='shipyard_ships'
    )
    crew = models.ForeignKey(
        ShipCrew,
        on_delete=models.CASCADE,
    )

    @classmethod
    def add(cls, shipyard_ship_data, frame, reactor, engine, modules: List[Module], mounts: List[Mount], crew):
        shipyard_ship, created = cls.objects.update_or_create(
            ship_type=shipyard_ship_data['type'],
            name=shipyard_ship_data['name'],
            description=shipyard_ship_data['description'],
            frame=frame,
            reactor=reactor,
            engine=engine,
            crew=crew,
            defaults={
                'ship_type': shipyard_ship_data['type'],
                'name': shipyard_ship_data['name'],
                'description': shipyard_ship_data['description'],
                'frame': frame,
                'reactor': reactor,
                'engine': engine,
                'crew': crew
            }
        )

        # TODO look into `bulk_create`
        for module in modules:
            ShipyardShipModuleLink.add(shipyard_ship, module)

        for mount in mounts:
            ShipyardShipMountLink.add(shipyard_ship, mount)

        return shipyard_ship


class ShipyardShipModuleLink(models.Model):
    shipyard_ship = models.ForeignKey(
        ShipyardShip,
        on_delete=models.CASCADE,
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        choices=SHIP_MODULE_SYMBOL
    )

    @classmethod
    def add(cls, shipyard_ship, module):
        shipyard_ship_module_link, created = cls.objects.update_or_create(
            shipyard_ship=shipyard_ship,
            module=module,
            defaults={
                'shipyard_ship': shipyard_ship,
                'module': module
            }
        )
        return shipyard_ship_module_link


class ShipyardShipMountLink(models.Model):
    shipyard_ship = models.ForeignKey(
        ShipyardShip,
        on_delete=models.CASCADE,
    )
    mount = models.ForeignKey(
        Mount,
        on_delete=models.CASCADE,
        choices=SHIP_MOUNT_SYMBOL
    )

    @classmethod
    def add(cls, shipyard_ship, mount):
        shipyard_ship_mount_link, created = cls.objects.update_or_create(
            shipyard_ship=shipyard_ship,
            mount=mount,
            defaults={
                'shipyard_ship': shipyard_ship,
                'mount': mount
            }
        )
        return shipyard_ship_mount_link


class Shipyard(models.Model):
    waypoint = models.ForeignKey(
        'systems.Waypoint',
        on_delete=models.CASCADE,
    )
    # The API returns a list with ship types sold here, but you can get than info in the ships field
    # Might need to change this to a ManyToOneField
    ships = models.ManyToManyField(
        ShipyardShip,
        through='ShipyardShipLink',
        related_name='shipyards',
        verbose_name="the list of ship types available for purchase at this shipyard.."
    )
    modifications_fee = models.IntegerField(
        verbose_name="the fee to modify a ship at this shipyard. This includes installing or removing modules and mounts on a ship. In the case of mounts, the fee is a flat rate per mount. In the case of modules, the fee is per slot the module occupies."
    )

    @classmethod
    def add(cls, shipyard_data, waypoint):
        shipyard, created = cls.objects.update_or_create(
            waypoint=waypoint,
            defaults={
                'waypoint': waypoint,
                'modifications_fee': shipyard_data['modificationsFee']
            }
        )

        # TODO look into `bulk_create`
        for shipyard_ship_data in shipyard_data['ships']:
            shipyard_ship = ShipyardShip.add(
                shipyard_ship_data,
                Frame.add(shipyard_ship_data['frame']),
                Reactor.add(shipyard_ship_data['reactor']),
                Engine.add(shipyard_ship_data['engine']),
                [Module.add(module) for module in shipyard_ship_data['modules']],
                [Mount.add(mount, shipyard_ship_data['deposits']) for mount in shipyard_ship_data['mounts']],
                ShipCrew.add(shipyard_ship_data['crew'])
            )
            ShipyardShipLink.add(shipyard_ship_data, shipyard, shipyard_ship)
        return shipyard


class ShipyardShipLink(models.Model):
    shipyard = models.ForeignKey(
        Shipyard,
        on_delete=models.CASCADE,
    )
    shipyard_ship = models.ForeignKey(
        ShipyardShip,
        on_delete=models.CASCADE,
    )
    purchase_price = models.IntegerField(
        verbose_name="the price of the ship at this shipyard."
    )
    supply = models.CharField(
        max_length=500,
        choices=MARKET_SUPPLY,
        verbose_name="the supply of the ship at this shipyard."
    )
    activity = models.CharField(
        max_length=500,
        choices=MARKET_ACTIVITY,
        verbose_name="the activity level of a trade good. If the good is an import, this represents how strong consumption is for the good. If the good is an export, this represents how strong the production is for the good."
    )

    @classmethod
    def add(cls, shipyard_ship_data, shipyard, shipyard_ship):
        shipyard_ship_link, created = cls.objects.update_or_create(
            shipyard=shipyard,
            shipyard_ship=shipyard_ship,
            defaults={
                'shipyard': shipyard,
                'shipyard_ship': shipyard_ship,
                'purchase_price': shipyard_ship_data['purchasePrice'],
                'supply': shipyard_ship_data['supply'],
                'activity': shipyard_ship_data['activity']
            }
        )
        return shipyard_ship_link


class ShipyardTransaction(models.Model):
    shipyard = models.ForeignKey(
        Shipyard,
        verbose_name="the symbol of the waypoint where the transaction took place.",
        on_delete=models.CASCADE,
    )
    ship = models.ForeignKey(
        # TODO make sure that this is a ship and not shipyard ship
        Ship,
        verbose_name="the symbol of the ship that was the subject of the transaction.",
        on_delete=models.CASCADE,
    )
    price = models.IntegerField(
        verbose_name='the price of the transaction.',
        validators=[MinValueValidator(0)]
    )
    agent_symbol = models.ForeignKey(
        'agents.Agent',
        verbose_name="the symbol of the agent that made the transaction.",
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField()

    @classmethod
    def add(cls, shipyard_transaction_data, shipyard, ship, agent):
        shipyard_transaction, created = cls.objects.update_or_create(
            shipyard=shipyard,
            ship=ship,
            price=shipyard_transaction_data['price'],
            agent_symbol=agent,
            timestamp=shipyard_transaction_data['timestamp'],
            defaults={
                'shipyard': shipyard,
                'ship': ship,
                'price': shipyard_transaction_data['price'],
                'agent_symbol': agent,
                'timestamp': shipyard_transaction_data['timestamp']
            }
        )
        return shipyard_transaction
