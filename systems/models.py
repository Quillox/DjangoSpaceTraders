from django.db import models
from django.core.validators import MinValueValidator
from django.apps import apps

from factions.models import Faction

SYSTEM_TYPE = [
    ('NEUTRON_STAR', 'Neutron Star'),
    ('RED_STAR', 'Red Star'),
    ('ORANGE_STAR', 'Orange Star'),
    ('BLUE_STAR', 'Blue Star'),
    ('YOUNG_STAR', 'Young Star'),
    ('WHITE_DWARF', 'White Dwarf'),
    ('BLACK_HOLE', 'Black Hole'),
    ('HYPERGIANT', 'Hypergiant'),
    ('NEBULA', 'Nebula'),
    ('UNSTABLE', 'Unstable')
]

WAYPOINT_TYPE = [
    ('PLANET', 'Planet'),
    ('GAS_GIANT', 'Gas Giant'),
    ('MOON', 'Moon'),
    ('ORBITAL_STATION', 'Orbital Station'),
    ('JUMP_GATE', 'Jump Gate'),
    ('ASTEROID_FIELD', 'Asteroid Field'),
    ('ASTEROID', 'Asteroid'),
    ('ENGINEERED_ASTEROID', 'Engineered Asteroid'),
    ('ASTEROID_BASE', 'Asteroid Base'),
    ('NEBULA', 'Nebula'),
    ('DEBRIS_FIELD', 'Debris Field'),
    ('GRAVITY_WELL', 'Gravity Well'),
    ('ARTIFICIAL_GRAVITY_WELL', 'Artificial Gravity Well'),
    ('FUEL_STATION', 'Fuel Station')
]

WAYPOINT_TRAIT_SYMBOL = [
    ('UNCHARTED', 'Uncharted'),
    ('MARKETPLACE', 'Marketplace'),
    ('SHIPYARD', 'Shipyard'),
    ('OUTPOST', 'Outpost'),
    ('SCATTERED_SETTLEMENTS', 'Scattered Settlements'),
    ('SPRAWLING_CITIES', 'Sprawling Cities'),
    ('MEGA_STRUCTURES', 'Mega Structures'),
    ('OVERCROWDED', 'Overcrowded'),
    ('HIGH_TECH', 'High Tech'),
    ('CORRUPT', 'Corrupt'),
    ('BUREAUCRATIC', 'Bureaucratic'),
    ('TRADING_HUB', 'Trading Hub'),
    ('INDUSTRIAL', 'Industrial'),
    ('BLACK_MARKET', 'Black Market'),
    ('RESEARCH_FACILITY', 'Research Facility'),
    ('MILITARY_BASE', 'Military Base'),
    ('SURVEILLANCE_OUTPOST', 'Surveillance Outpost'),
    ('EXPLORATION_OUTPOST', 'Exploration Outpost'),
    ('MINERAL_DEPOSITS', 'Mineral Deposits'),
    ('COMMON_METAL_DEPOSITS', 'Common Metal Deposits'),
    ('PRECIOUS_METAL_DEPOSITS', 'Precious Metal Deposits'),
    ('RARE_METAL_DEPOSITS', 'Rare Metal Deposits'),
    ('METHANE_POOLS', 'Methane Pools'),
    ('ICE_CRYSTALS', 'Ice Crystals'),
    ('EXPLOSIVE_GASES', 'Explosive Gases'),
    ('STRONG_MAGNETOSPHERE', 'Strong Magnetosphere'),
    ('VIBRANT_AURORAS', 'Vibrant Auroras'),
    ('SALT_FLATS', 'Salt Flats'),
    ('CANYONS', 'Canyons'),
    ('PERPETUAL_DAYLIGHT', 'Perpetual Daylight'),
    ('PERPETUAL_OVERCAST', 'Perpetual Overcast'),
    ('DRY_SEABEDS', 'Dry Seabeds'),
    ('MAGMA_SEAS', 'Magma Seas'),
    ('SUPERVOLCANOES', 'Supervolcanoes'),
    ('ASH_CLOUDS', 'Ash Clouds'),
    ('VAST_RUINS', 'Vast Ruins'),
    ('MUTATED_FLORA', 'Mutated Flora'),
    ('TERRAFORMED', 'Terraformed'),
    ('EXTREME_TEMPERATURES', 'Extreme Temperatures'),
    ('EXTREME_PRESSURE', 'Extreme Pressure'),
    ('DIVERSE_LIFE', 'Diverse Life'),
    ('SCARCE_LIFE', 'Scarce Life'),
    ('FOSSILS', 'Fossils'),
    ('WEAK_GRAVITY', 'Weak Gravity'),
    ('STRONG_GRAVITY', 'Strong Gravity'),
    ('CRUSHING_GRAVITY', 'Crushing Gravity'),
    ('TOXIC_ATMOSPHERE', 'Toxic Atmosphere'),
    ('CORROSIVE_ATMOSPHERE', 'Corrosive Atmosphere'),
    ('BREATHABLE_ATMOSPHERE', 'Breathable Atmosphere'),
    ('JOVIAN', 'Jovian'),
    ('ROCKY', 'Rocky'),
    ('VOLCANIC', 'Volcanic'),
    ('FROZEN', 'Frozen'),
    ('SWAMP', 'Swamp'),
    ('BARREN', 'Barren'),
    ('TEMPERATE', 'Temperate'),
    ('JUNGLE', 'Jungle'),
    ('OCEAN', 'Ocean'),
    ('STRIPPED', 'Stripped')
]

WAYPOINT_MODIFIER_SYMBOL = [
    ('STRIPPED', 'Stripped'),
    ('UNSTABLE', 'Unstable'),
    ('RADIATION_LEAK', 'Radiation Leak'),
    ('CRITICAL_LIMIT', 'Critical Limit'),
    ('CIVIL_UNREST', 'Civil Unrest')
]

TRADE_TYPE = [
    ('EXPORT', 'Export'),
    ('IMPORT', 'Import'),
    ('EXCHANGE', 'Exchange')
]

TRANSACTION_TYPE = [
    ('PURCHASE', 'Purchase'),
    ('SELL', 'Sell')
]

MARKET_SUPPLY = [
    ('SCARCE', 'Scarce'),
    ('LIMITED', 'Limited'),
    ('MODERATE', 'Moderate'),
    ('HIGH', 'High'),
    ('ABUNDANT', 'Abundant')
]

MARKET_ACTIVITY = [
    ('WEAK', 'Weak'),
    ('GROWING', 'Growing'),
    ('STRONG', 'Strong')
]

TRADE_GOOD_SYMBOLS = [
    ('PRECIOUS_STONES', 'Precious Stones'),
    ('QUARTZ_SAND', 'Quartz Sand'),
    ('SILICON_CRYSTALS', 'Silicon Crystals'),
    ('AMMONIA_ICE', 'Ammonia Ice'),
    ('LIQUID_HYDROGEN', 'Liquid Hydrogen'),
    ('LIQUID_NITROGEN', 'Liquid Nitrogen'),
    ('ICE_WATER', 'Ice Water'),
    ('EXOTIC_MATTER', 'Exotic Matter'),
    ('ADVANCED_CIRCUITRY', 'Advanced Circuitry'),
    ('GRAVITON_EMITTERS', 'Graviton Emitters'),
    ('IRON', 'Iron'),
    ('IRON_ORE', 'Iron Ore'),
    ('COPPER', 'Copper'),
    ('COPPER_ORE', 'Copper Ore'),
    ('ALUMINUM', 'Aluminum'),
    ('ALUMINUM_ORE', 'Aluminum Ore'),
    ('SILVER', 'Silver'),
    ('SILVER_ORE', 'Silver Ore'),
    ('GOLD', 'Gold'),
    ('GOLD_ORE', 'Gold Ore'),
    ('PLATINUM', 'Platinum'),
    ('PLATINUM_ORE', 'Platinum Ore'),
    ('DIAMONDS', 'Diamonds'),
    ('URANITE', 'Uranite'),
    ('URANITE_ORE', 'Uranite Ore'),
    ('MERITIUM', 'Meritium'),
    ('MERITIUM_ORE', 'Meritium Ore'),
    ('HYDROCARBON', 'Hydrocarbon'),
    ('ANTIMATTER', 'Antimatter'),
    ('FERTILIZERS', 'Fertilizers'),
    ('FABRICS', 'Fabrics'),
    ('FOOD', 'Food'),
    ('JEWELRY', 'Jewelry'),
    ('MACHINERY', 'Machinery'),
    ('FIREARMS', 'Firearms'),
    ('ASSAULT_RIFLES', 'Assault Rifles'),
    ('MILITARY_EQUIPMENT', 'Military Equipment'),
    ('EXPLOSIVES', 'Explosives'),
    ('LAB_INSTRUMENTS', 'Lab Instruments'),
    ('AMMUNITION', 'Ammunition'),
    ('ELECTRONICS', 'Electronics'),
    ('SHIP_PLATING', 'Ship Plating'),
    ('EQUIPMENT', 'Equipment'),
    ('FUEL', 'Fuel'),
    ('MEDICINE', 'Medicine'),
    ('DRUGS', 'Drugs'),
    ('CLOTHING', 'Clothing'),
    ('MICROPROCESSORS', 'Microprocessors'),
    ('PLASTICS', 'Plastics'),
    ('POLYNUCLEOTIDES', 'Polynucleotides'),
    ('BIOCOMPOSITES', 'Biocomposites'),
    ('NANOBOTS', 'Nanobots'),
    ('AI_MAINFRAMES', 'Ai Mainframes'),
    ('QUANTUM_DRIVES', 'Quantum Drives'),
    ('ROBOTIC_DRONES', 'Robotic Drones'),
    ('CYBER_IMPLANTS', 'Cyber Implants'),
    ('GENE_THERAPEUTICS', 'Gene Therapeutics'),
    ('NEURAL_CHIPS', 'Neural Chips'),
    ('MOOD_REGULATORS', 'Mood Regulators'),
    ('VIRAL_AGENTS', 'Viral Agents'),
    ('MICRO_FUSION_GENERATORS', 'Micro Fusion Generators'),
    ('SUPERGRAINS', 'Supergrains'),
    ('LASER_RIFLES', 'Laser Rifles'),
    ('HOLOGRAPHICS', 'Holographics'),
    ('SHIP_SALVAGE', 'Ship Salvage'),
    ('RELIC_TECH', 'Relic Tech'),
    ('NOVEL_LIFEFORMS', 'Novel Lifeforms'),
    ('BOTANICAL_SPECIMENS', 'Botanical Specimens'),
    ('CULTURAL_ARTIFACTS', 'Cultural Artifacts'),
    ('REACTOR_SOLAR_I', 'Reactor Solar I'),
    ('REACTOR_FUSION_I', 'Reactor Fusion I'),
    ('REACTOR_FISSION_I', 'Reactor Fission I'),
    ('REACTOR_CHEMICAL_I', 'Reactor Chemical I'),
    ('REACTOR_ANTIMATTER_I', 'Reactor Antimatter I'),
    ('ENGINE_IMPULSE_DRIVE_I', 'Engine Impulse Drive I'),
    ('ENGINE_ION_DRIVE_I', 'Engine Ion Drive I'),
    ('ENGINE_ION_DRIVE_II', 'Engine Ion Drive II'),
    ('ENGINE_HYPER_DRIVE_I', 'Engine Hyper Drive I'),
    ('MODULE_MINERAL_PROCESSOR_I', 'Module Mineral Processor I'),
    ('MODULE_CARGO_HOLD_I', ' Module Cargo Hold I'),
    ('MODULE_CREW_QUARTERS_I', ' Module Crew Quarters I'),
    ('MODULE_ENVOY_QUARTERS_I', ' Module Envoy Quarters I'),
    ('MODULE_PASSENGER_CABIN_I', ' Module Passenger Cabin I'),
    ('MODULE_MICRO_REFINERY_I', ' Module Micro Refinery_I'),
    ('MODULE_ORE_REFINERY_I', ' Module Ore Refinery_I'),
    ('MODULE_FUEL_REFINERY_I', ' Module Fuel Refinery I'),
    ('MODULE_SCIENCE_LAB_I', ' Module Science Lab I'),
    ('MODULE_WARP_DRIVE_I', ' Module Warp Drive I'),
    ('MODULE_WARP_DRIVE_II', ' Module Warp Drive II'),
    ('MODULE_WARP_DRIVE_III', ' Module Warp Drive III'),
    ('MODULE_SHIELD_GENERATOR_I', ' Module Shield Generator I'),
    ('MODULE_SHIELD_GENERATOR_II', ' Module Shield Generator II'),
    ('MOUNT_GAS_SIPHON_I', 'Mount Gas Siphon_I'),
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
    ('MOUNT_TURRET_I', 'Mount Turret I'),
]


def get_sector_system_waypoint(symbol):
    try:
        if len(symbol.split('-')) == 3:
            sector = symbol.split('-')[0]
            system = symbol.split('-')[0] + '-' + symbol.split('-')[1]
            waypoint = symbol
        elif len(symbol.split('-')) == 2:
            sector = symbol.split('-')[0]
            system = symbol.split('-')[0] + '-' + symbol.split('-')[1]
            waypoint = None
        elif len(symbol.split('-')) == 1:
            sector = symbol
            system = None
            waypoint = None
    except:
        print(f'Error: {symbol} is not a valid symbol!')
        return {'sector': None, 'system': None, 'waypoint': None}
    else:
        return {'sector': sector, 'system': system, 'waypoint': waypoint}


class TradeGood(models.Model):
    symbol = models.CharField(
        primary_key=True,
        max_length=500,
        choices=TRADE_GOOD_SYMBOLS
    )
    # These might have to be nullable
    name = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )
    description = models.CharField(
        max_length=5000,
        null=True,
        blank=True
    )

    # TODO work out how to update the trade goods table without overwriting the name and description with None
    @classmethod
    def add(cls, trade_good_data):
        if trade_good_data.get('name'):
            name = trade_good_data['name']
        else:
            name = None
        if trade_good_data.get('description'):
            description = trade_good_data['description']
        else:
            description = None
        trade_good, created = cls.objects.update_or_create(
            symbol=trade_good_data['symbol'],
            defaults={
                'symbol': trade_good_data['symbol'],
                'name': name,
                'description': description
            }
        )
        return trade_good


class System(models.Model):
    symbol = models.CharField(
        primary_key=True,
        max_length=500
    )
    sector_symbol = models.CharField(
        max_length=500
    )
    system_type = models.CharField(
        max_length=500,
        choices=SYSTEM_TYPE
    )
    x = models.IntegerField(
        verbose_name="relative position of the system in the sector in the x axis."
    )
    y = models.IntegerField(
        verbose_name="relative position of the system in the sector in the y axis."
    )
    factions = models.ManyToManyField(
        Faction,
        through='SystemFactionLink',
        related_name='systems'
    )

    def __str__(self) -> str:
        return f'{self.system_type} ({self.symbol}) with {self.waypoints.count()} known waypoints.'

    @classmethod
    def add(cls, system_data):
        print(f'Adding system {system_data["symbol"]} to the database...')
        system, created = cls.objects.update_or_create(
            symbol=system_data['symbol'],
            defaults={
                'symbol': system_data['symbol'],
                'sector_symbol': system_data['sectorSymbol'],
                'system_type': system_data['type'],
                'x': system_data['x'],
                'y': system_data['y']
            }
        )
        for faction_data in system_data.get('factions'):
            if faction_data:
                faction = Faction.objects.get(symbol=faction_data['symbol'])
                SystemFactionLink.add(system, faction)
            else:
                continue
        return system


class SystemFactionLink(models.Model):
    system = models.ForeignKey(
        System,
        on_delete=models.CASCADE,
    )
    faction = models.ForeignKey(
        Faction,
        on_delete=models.CASCADE,
    )

    @classmethod
    def add(cls, system, faction):
        system_faction_link, created = cls.objects.update_or_create(
            system=system,
            faction=faction,
            defaults={
                'system': system,
                'faction': faction
            }
        )
        return system_faction_link


class Waypoint(models.Model):
    # TODO if the waypoint is a jump gate, then show this in the `waypoint_detail.html` template.
    symbol = models.CharField(
        primary_key=True,
        max_length=500
    )
    system = models.ForeignKey(
        System,
        on_delete=models.CASCADE,
        related_name='waypoints'
    )
    waypoint_type = models.CharField(
        max_length=500,
        choices=WAYPOINT_TYPE
    )
    x = models.IntegerField(
        verbose_name="relative position of the waypoint in the system in the x axis."
    )
    y = models.IntegerField(
        verbose_name="relative position of the waypoint in the system in the y axis."
    )
    orbits = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name="the symbol of the parent waypoint, if this waypoint is in orbit around another waypoint. Otherwise this value is undefined.",
        null=True
    )
    faction = models.ForeignKey(
        'factions.Faction',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    traits = models.ManyToManyField(
        'WaypointTrait',
        through='WaypointTraitLink',
        related_name='waypoints'
    )
    modifiers = models.ManyToManyField(
        'WaypointModifier',
        through='WaypointModifierLink',
        related_name='waypoints'
    )
    is_under_construction = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        ans = f'{self.symbol} - {self.waypoint_type} ({self.x}, {self.y})'
        return ans

    @classmethod
    def add(cls, waypoint_data):
        system_symbol = get_sector_system_waypoint(waypoint_data['symbol'])['system']
        if waypoint_data.get('orbits'):
            parent_waypoint = Waypoint.objects.get(
                symbol=waypoint_data.get('orbits'))
        else:
            parent_waypoint = None
        if waypoint_data.get('faction'):
            faction = Faction.objects.get(symbol=waypoint_data['faction']['symbol'])
        else:
            faction = None
        if waypoint_data.get('isUnderConstruction'):
            is_under_construction = waypoint_data['isUnderConstruction']
        else:
            is_under_construction = None
        waypoint, created = cls.objects.update_or_create(
            symbol=waypoint_data['symbol'],
            defaults={
                'symbol': waypoint_data['symbol'],
                'system': System.objects.get(symbol=system_symbol),
                'waypoint_type': waypoint_data['type'],
                'x': waypoint_data['x'],
                'y': waypoint_data['y'],
                'orbits': parent_waypoint,
                'faction': faction,
                'is_under_construction': is_under_construction
            }
        )
        for trait in waypoint_data.get('traits', []):
            if trait:
                waypoint_trait = WaypointTrait.add(trait)
                WaypointTraitLink.add(waypoint, waypoint_trait)
            else:
                continue
        for modifier in waypoint_data.get('modifiers', []):
            if modifier:
                waypoint_modifier = WaypointModifier.add(modifier)
                WaypointModifierLink.add(waypoint, waypoint_modifier)
            else:
                continue
        if created:
            print(f'\tWaypoint {waypoint.symbol} added to the database.')
        else:
            print(f'\tWaypoint {waypoint.symbol} updated in the database.')
        return waypoint

    def update(self, waypoint_data):
        # TODO deal with adding chart
        if waypoint_data.get('orbits'):
            parent_waypoint = Waypoint.objects.get(
                symbol=waypoint_data.get('orbits'))
        else:
            parent_waypoint = None
        if waypoint_data.get('faction'):
            faction = Faction.objects.get(symbol=waypoint_data['faction']['symbol'])
        else:
            faction = None
        if waypoint_data.get('isUnderConstruction'):
            is_under_construction = waypoint_data['isUnderConstruction']
        else:
            is_under_construction = None
        self.symbol = waypoint_data['symbol']
        self.system = System.objects.get(symbol=waypoint_data['systemSymbol'])
        self.waypoint_type = waypoint_data['type']
        self.x = waypoint_data['x']
        self.y = waypoint_data['y']
        self.orbits = parent_waypoint
        self.faction = faction
        self.is_under_construction = is_under_construction
        self.save()
        for trait in waypoint_data.get('traits', []):
            if trait:
                waypoint_trait = WaypointTrait.add(trait)
                WaypointTraitLink.add(self, waypoint_trait)
            else:
                continue
        for modifier in waypoint_data.get('modifiers', []):
            if modifier:
                waypoint_modifier = WaypointModifier.add(modifier)
                WaypointModifierLink.add(self, waypoint_modifier)
            else:
                continue
        self.save()
        print(f'\tWaypoint {self.symbol} updated in the database.')
        return self


class WaypointTrait(models.Model):
    symbol = models.CharField(
        primary_key=True,
        max_length=500,
        choices=WAYPOINT_TRAIT_SYMBOL
    )
    name = models.CharField(
        max_length=500
    )
    description = models.CharField(
        max_length=5000
    )

    def __str__(self) -> str:
        return f'{self.name}: {self.description}'

    @classmethod
    def add(cls, waypoint_trait_data):
        waypoint_trait, created = cls.objects.update_or_create(
            symbol=waypoint_trait_data['symbol'],
            defaults={
                'symbol': waypoint_trait_data['symbol'],
                'name': waypoint_trait_data['name'],
                'description': waypoint_trait_data['description']
            }
        )
        return waypoint_trait


class WaypointTraitLink(models.Model):
    waypoint = models.ForeignKey(
        Waypoint,
        on_delete=models.CASCADE,
        related_name='trait_links'
    )
    # TODO rename to trait
    trait = models.ForeignKey(
        WaypointTrait,
        on_delete=models.CASCADE,
        related_name='waypoint_links'
    )

    @classmethod
    def add(cls, waypoint, waypoint_trait):
        waypoint_trait_link, created = cls.objects.update_or_create(
            waypoint=waypoint,
            trait=waypoint_trait,
            defaults={
                'waypoint': waypoint,
                'trait': waypoint_trait
            }
        )
        return waypoint_trait_link

class ConstructionSite(models.Model):
    waypoint = models.ForeignKey(
        Waypoint,
        on_delete=models.CASCADE,
        related_name='construction_site'
    )
    TradeGood = models.ForeignKey(
        TradeGood,
        on_delete=models.CASCADE,
        related_name='construction_site'
    )
    required = models.IntegerField(
        verbose_name="the number of units of the trade good required to complete construction of the waypoint.",
    )
    fulfilled = models.IntegerField(
        verbose_name="the number of units of the trade good that have been delivered to the construction site.",
    )

    @classmethod
    def add(cls, waypoint, trade_good, required, fulfilled):
        construction_site, created = cls.objects.update_or_create(
            waypoint=waypoint,
            TradeGood=trade_good,
            defaults={
                'waypoint': waypoint,
                'TradeGood': trade_good,
                'required': required,
                'fulfilled': fulfilled
            }
        )
        return construction_site


class WaypointModifier(models.Model):
    symbol = models.CharField(
        primary_key=True,
        max_length=500,
        choices=WAYPOINT_MODIFIER_SYMBOL
    )
    name = models.CharField(
        max_length=500
    )
    description = models.CharField(
        max_length=5000
    )

    def __str__(self) -> str:
        return f'{self.name}: {self.description}'

    @classmethod
    def add(cls, waypoint_modifier_data):
        waypoint_modifier, created = cls.objects.update_or_create(
            symbol=waypoint_modifier_data['symbol'],
            defaults={
                'symbol': waypoint_modifier_data['symbol'],
                'name': waypoint_modifier_data['name'],
                'description': waypoint_modifier_data['description']
            }
        )
        return waypoint_modifier


class WaypointModifierLink(models.Model):
    waypoint = models.ForeignKey(
        Waypoint,
        on_delete=models.CASCADE,
    )
    waypoint_modifier = models.ForeignKey(
        WaypointModifier,
        on_delete=models.CASCADE,
    )

    @classmethod
    def add(cls, waypoint, waypoint_modifier):
            waypoint_modifier_link, created = cls.objects.update_or_create(
                waypoint=waypoint,
                defaults={
                    'waypoint': waypoint,
                    'waypoint_modifier': waypoint_modifier
                }
            )
            return waypoint_modifier_link


class Chart(models.Model):
    waypoint = models.OneToOneField(
        Waypoint,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="The chart of a system or waypoint, which makes the location visible to other agents.",
        related_name='chart'
    )
    submitted_by = models.ForeignKey(
        'agents.Agent',
        on_delete=models.CASCADE,
        verbose_name="the agent that submitted the chart for this waypoint."
    )
    submitted_on = models.DateTimeField(
        verbose_name="the date and time the chart was submitted."
    )

    def __str__(self):
        return f'{self.waypoint.symbol} charted by {self.submitted_by} on {self.submitted_on}'

    @classmethod
    def add(cls, waypoint, agent, submitted_on):
        chart, created = cls.objects.update_or_create(
            waypoint=waypoint,
            defaults={
                'waypoint': waypoint,
                'submitted_by': agent,
                'submitted_on': submitted_on
            }
        )
        return chart


class Market(models.Model):
    waypoint = models.OneToOneField(
        Waypoint,
        on_delete=models.CASCADE,
        related_name='market',
        primary_key=True
    )
    exports = models.ManyToManyField(
        TradeGood,
        through='MarketExportLink',
        related_name='exports',
        verbose_name="the list of goods that are exported from this market."
    )
    imports = models.ManyToManyField(
        TradeGood,
        through='MarketImportLink',
        related_name='imports',
        verbose_name="the list of goods that are sought as imports in this market."
    )
    exchanges = models.ManyToManyField(
        TradeGood,
        through='MarketExchangeLink',
        related_name='exchanges',
        verbose_name="the list of goods that are bought and sold between agents at this market."
    )
    trade_goods = models.ManyToManyField(
        TradeGood,
        through='MarketTradeGoodLink',
        related_name='market',
        verbose_name="the list of goods that are traded at this market. Visible only when a ship is present at the market.",
        blank=True
    )

    @classmethod
    def add(cls, market_data):
        # Avoids circular import
        Ship = apps.get_model('fleet', 'Ship')

        market, created = cls.objects.update_or_create(
            waypoint=Waypoint.objects.get(symbol=market_data['symbol']),
            defaults={
                'waypoint': Waypoint.objects.get(symbol=market_data['symbol'])
            }
        )
        for trade_good_data in market_data.get('exports', []):
            if trade_good_data:
                trade_good = TradeGood.add(trade_good_data)
                MarketExportLink.add(market, trade_good)
        for trade_good_data in market_data.get('imports', []):
            if trade_good_data:
                trade_good = TradeGood.add(trade_good_data)
                MarketImportLink.add(market, trade_good)
        for trade_good_data in market_data.get('exchange', []):
            if trade_good_data:
                trade_good = TradeGood.add(trade_good_data)
                MarketExchangeLink.add(market, trade_good)
        for trade_good_data in market_data.get('tradeGoods', []):
            if trade_good_data:
                trade_good = TradeGood.add(trade_good_data)
                MarketTradeGoodLink.add(trade_good_data, market, trade_good)
            else:
                continue
        for transaction_data in market_data.get('transactions', []):
            if transaction_data:
                ship = Ship.objects.get(symbol=transaction_data['shipSymbol'])
                trade_good = TradeGood.objects.get(symbol=transaction_data['tradeSymbol'])
                MarketTransaction.add(transaction_data, market, ship, trade_good)
            else:
                continue
        if created:
            print(f'\t\tMarket {market.waypoint} added to the database.')
        else:
            print(f'\t\tMarket {market.waypoint} updated in the database.')
        return market


class MarketExportLink(models.Model):
    market = models.ForeignKey(
        Market,
        on_delete=models.CASCADE,
    )
    trade_good = models.ForeignKey(
        TradeGood,
        on_delete=models.CASCADE,
    )

    @classmethod
    def add(cls, market, trade_good):
        market_export_link, created = cls.objects.update_or_create(
            market=market,
            trade_good=trade_good,
            defaults={
                'market': market,
                'trade_good': trade_good
            }
        )
        return market_export_link


class MarketImportLink(models.Model):
    market = models.ForeignKey(
        Market,
        on_delete=models.CASCADE,
    )
    trade_good = models.ForeignKey(
        TradeGood,
        on_delete=models.CASCADE,
    )

    @classmethod
    def add(cls, market, trade_good):
        market_import_link, created = cls.objects.update_or_create(
            market=market,
            trade_good=trade_good,
            defaults={
                'market': market,
                'trade_good': trade_good
            }
        )
        return market_import_link


class MarketExchangeLink(models.Model):
    market = models.ForeignKey(
        Market,
        on_delete=models.CASCADE,
    )
    trade_good = models.ForeignKey(
        TradeGood,
        on_delete=models.CASCADE,
    )

    @classmethod
    def add(cls, market, trade_good):
        market_exchange_link, created = cls.objects.update_or_create(
            market=market,
            trade_good=trade_good,
            defaults={
                'market': market,
                'trade_good': trade_good
            }
        )
        return market_exchange_link


class MarketTradeGoodLink(models.Model):
    market = models.ForeignKey(
        Market,
        on_delete=models.CASCADE,
    )
    trade_good = models.ForeignKey(
        TradeGood,
        on_delete=models.CASCADE,
    )
    trade_type = models.CharField(
        max_length=500,
        choices=TRADE_TYPE
    )
    volume = models.IntegerField(
        verbose_name="the maximum number of units that can be purchased or sold at this market in a single trade for this good. Trade volume also gives an indication of price volatility. A market with a low trade volume will have large price swings, while high trade volume will be more resilient to price changes.",
        validators=[MinValueValidator(1)]
    )
    supply = models.CharField(
        max_length=500,
        choices=MARKET_SUPPLY
    )
    activity = models.CharField(
        max_length=500,
        verbose_name="the activity level of a trade good. If the good is an import, this represents how strong consumption is for the good. If the good is an export, this represents how strong the production is for the good.",
        choices=MARKET_ACTIVITY,
        null=True,
        blank=True
    )
    purchase_price = models.IntegerField(
        verbose_name="the price at which this good can be purchased from the market.",
        validators=[MinValueValidator(0)]
    )
    sell_price = models.IntegerField(
        verbose_name="the price at which this good can be sold to the market.",
        validators=[MinValueValidator(0)]
    )

    @classmethod
    def add(cls, trade_data, market, trade_good):
        if trade_data.get('activity'):
            activity = trade_data['activity']
        else:
            activity = None

        market_trade_good_link, created = cls.objects.update_or_create(
            market=market,
            trade_good=trade_good,
            defaults={
                'market': market,
                'trade_good': trade_good,
                'trade_type': trade_data['type'],
                'volume': trade_data['tradeVolume'],
                'supply': trade_data['supply'],
                'activity': activity,
                'purchase_price': trade_data['purchasePrice'],
                'sell_price': trade_data['sellPrice']
            }
        )
        return market_trade_good_link

    def __str__(self) -> str:
        out = f'{self.trade_good}: '
        if self.trade_type == 'EXPORT':
            out += f'sell price: {self.sell_price}, '
        elif self.trade_type == 'IMPORT':
            out += f'purchase price: {self.purchase_price}, '
        return out + f'volume: {self.volume}, supply: {self.supply}, activity: {self.activity}'
class MarketTransaction(models.Model):
    market = models.ForeignKey(
        Market,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    ship = models.ForeignKey(
        'fleet.Ship',
        on_delete=models.CASCADE,
        related_name='market_transactions'
    )
    trade_good = models.ForeignKey(
        TradeGood,
        on_delete=models.CASCADE,
    )
    transaction_type = models.CharField(
        max_length=500,
        choices=TRANSACTION_TYPE
    )
    units = models.IntegerField(
        verbose_name="the number of units of the transaction.",
        validators=[MinValueValidator(0)]
    )
    price_per_unit = models.IntegerField(
        verbose_name="the price per unit of the transaction.",
        validators=[MinValueValidator(0)]
    )
    total_price = models.IntegerField(
        verbose_name="the total price of the transaction.",
        validators=[MinValueValidator(0)]
    )
    timestamp = models.DateTimeField(
        verbose_name="the date and time the transaction was made."
    )

    @classmethod
    def add(cls, transactions_data, market, ship, trade_good):
        market_transaction, created = cls.objects.update_or_create(
            market=market,
            ship=ship,
            trade_good=trade_good,
            transaction_type=transactions_data['type'],
            units=transactions_data['units'],
            price_per_unit=transactions_data['pricePerUnit'],
            total_price=transactions_data['totalPrice'],
            timestamp=transactions_data['timestamp'],
            defaults={
                'market': market,
                'ship': ship,
                'trade_good': trade_good,
                'transaction_type': transactions_data['type'],
                'units': transactions_data['units'],
                'price_per_unit': transactions_data['pricePerUnit'],
                'total_price': transactions_data['totalPrice'],
                'timestamp': transactions_data['timestamp']
            }
        )
        return market_transaction


class JumpGate(models.Model):
    waypoint = models.ForeignKey(
        Waypoint,
        on_delete=models.CASCADE,
        related_name='jump_gate',
    )
    destination = models.ForeignKey(
        Waypoint,
        on_delete=models.CASCADE,
        related_name='jump_gate_origins',
    )

    @classmethod
    def add(cls, waypoint, destination):
        jump_gate, created = cls.objects.update_or_create(
            waypoint=waypoint,
            destination=destination,
            defaults={
                'waypoint': waypoint,
                'destination': destination
            }
        )
        if created:
            print(f'Jump gate {jump_gate.waypoint} to {jump_gate.destination} added to the database.')
        else:
            print(f'Jump gate {jump_gate.waypoint} to {jump_gate.destination} updated in the database.')
        return jump_gate