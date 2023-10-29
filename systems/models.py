from django.db import models
from django.core.validators import MinValueValidator

from factions.models import Faction
from fleet.models import Ship

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

TRANSACTION_TYPE = [
    ('PURCHASE', 'Purchase'),
    ('SELL', 'Sell')
]

MARKET_SUPPLY = [
    ('SCARCE', 'Scarce'),
    ('LIMITED', 'Limited'),
    ('MODERATE', 'Moderate'),
    ('ABUNDANT', 'Abundant')
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
        max_length=500
    )
    description = models.CharField(
        max_length=5000
    )

    @classmethod
    def add(cls, trade_good_data):
        trade_good, created = cls.objects.update_or_create(
            symbol=trade_good_data['symbol'],
            name=trade_good_data['name'],
            description=trade_good_data['description']
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
        system, created = cls.objects.update_or_create(
            symbol=system_data['symbol'],
            sector_symbol=system_data['sectorSymbol'],
            system_type=system_data['type'],
            x=system_data['x'],
            y=system_data['y']
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
            faction=faction
        )
        return system_faction_link


class Waypoint(models.Model):
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
        default=False
    )

    def __str__(self) -> str:
        ans = f'{self.symbol}: {self.waypoint_type} controlled by {self.faction} and is {", ".join([t.name for t in self.traits.all()])}.'
        ans_chart = f'Charted by {self.chart.submitted_by} on {self.chart.submitted_on}.'
        ans_no_chart = 'Uncharted.'
        ans_orbits = f'Orbits {self.orbits}.'
        if self.chart:
            ans += f' {ans_chart}'
        else:
            ans += f' {ans_no_chart}'
        if self.orbits:
            ans += f' {ans_orbits}'
        return ans

    def __repr__(self) -> str:
        return self.__str__()

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
        waypoint, created = cls.objects.update_or_create(
            symbol=waypoint_data['symbol'],
            system=System.objects.get(symbol=system_symbol),
            waypoint_type=waypoint_data['type'],
            x=waypoint_data['x'],
            y=waypoint_data['y'],
            orbits=parent_waypoint,
            faction=faction,
            is_under_construction=waypoint_data['isUnderConstruction']
        )
        for trait in waypoint_data.get('traits'):
            if trait:
                waypoint_trait = WaypointTrait.add(trait)
                WaypointTraitLink.add(waypoint, waypoint_trait)
            else:
                continue
        for modifier in waypoint_data.get('modifiers'):
            if modifier:
                waypoint_modifier = WaypointModifier.add(modifier)
                WaypointModifierLink.add(waypoint, waypoint_modifier)
            else:
                continue
        return waypoint


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
            name=waypoint_trait_data['name'],
            description=waypoint_trait_data['description']
        )
        return waypoint_trait


class WaypointTraitLink(models.Model):
    waypoint = models.ForeignKey(
        Waypoint,
        on_delete=models.CASCADE,
    )
    waypoint_trait = models.ForeignKey(
        WaypointTrait,
        on_delete=models.CASCADE,
    )

    @classmethod
    def add(cls, waypoint, waypoint_trait):
        waypoint_trait_link, created = cls.objects.update_or_create(
            waypoint=waypoint,
            waypoint_trait=waypoint_trait
        )
        return waypoint_trait_link


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
            name=waypoint_modifier_data['name'],
            description=waypoint_modifier_data['description']
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
                waypoint_modifier=waypoint_modifier
            )
            return waypoint_modifier_link


class Chart(models.Model):
    waypoint_symbol = models.OneToOneField(
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
        return f'{self.waypoint_symbol.symbol} charted by {self.submitted_by} on {self.submitted_on}'

    @classmethod
    def add(cls, waypoint, agent, submitted_on):
        chart, created = cls.objects.update_or_create(
            waypoint_symbol=waypoint,
            submitted_by=agent,
            submitted_on=submitted_on
        )
        return chart

class Market(models.Model):
    symbol = models.ForeignKey(
        Waypoint,
        on_delete=models.CASCADE,
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
        market, created = cls.objects.update_or_create(
            symbol=Waypoint.objects.get(symbol=market_data['symbol'])
        )
        for trade_good_data in market_data.get('exports'):
            if trade_good_data:
                trade_good = TradeGood.objects.get(symbol=trade_good_data['symbol'])
                MarketExportLink.add(market, trade_good)
            else:
                continue
        for trade_good_data in market_data.get('imports'):
            if trade_good_data:
                trade_good = TradeGood.objects.get(symbol=trade_good_data['symbol'])
                MarketImportLink.add(market, trade_good)
            else:
                continue
        for trade_good_data in market_data.get('exchanges'):
            if trade_good_data:
                trade_good = TradeGood.objects.get(symbol=trade_good_data['symbol'])
                MarketExchangeLink.add(market, trade_good)
            else:
                continue
        for trade_good_data in market_data.get('tradeGoods'):
            if trade_good_data:
                trade_good = TradeGood.objects.get(symbol=trade_good_data['symbol'])
                MarketTradeGoodLink.add(market, trade_good)
            else:
                continue
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
            trade_good=trade_good
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
            trade_good=trade_good
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
            trade_good=trade_good
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
    # TODO think about what extra information I could add here

    @classmethod
    def add(cls, market, trade_good):
        market_trade_good_link, created = cls.objects.update_or_create(
            market=market,
            trade_good=trade_good
        )
        return market_trade_good_link


class MarketTransaction(models.Model):
    market = models.ForeignKey(
        Market,
        on_delete=models.CASCADE,
    )
    ship_symbol = models.ForeignKey(
        'fleet.Ship',
        on_delete=models.CASCADE,
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
    def add(cls, transactions_data):
        market_transaction, created = cls.objects.update_or_create(
            market=Waypoint.objects.get(symbol=transactions_data['waypointSymbol']),
            ship_symbol=Ship.objects.get(symbol=transactions_data['shipSymbol']),
            trade_good=TradeGood.objects.get(symbol=transactions_data['tradeSymbol']),
            transaction_type=transactions_data['type'],
            units=transactions_data['units'],
            price_per_unit=transactions_data['pricePerUnit'],
            total_price=transactions_data['totalPrice'],
            timestamp=transactions_data['timestamp']
        )
        return market_transaction


class JumpGateLink(models.Model):
    jump_gate = models.ForeignKey(
        Waypoint,
        on_delete=models.CASCADE,
        related_name='jump_gate_link'
    )
    destination = models.ForeignKey(
        Waypoint,
        on_delete=models.CASCADE,
    )

    @classmethod
    def add(cls, jump_gate, destination):
        jump_gate_link, created = cls.objects.update_or_create(
            jump_gate=jump_gate,
            destination=destination
        )
        return jump_gate_link