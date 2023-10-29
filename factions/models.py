from django.db import models


FACTION_SYMBOLS = [
    ('COSMIC', 'Cosmic'),
    ('VOID', 'Void'),
    ('GALACTIC', 'Galactic'),
    ('QUANTUM', 'Quantum'),
    ('DOMINION', 'Dominion'),
    ('ASTRO', 'Astro'),
    ('CORSAIRS', 'Corsairs'),
    ('OBSIDIAN', 'Obsidian'),
    ('AEGIS', 'Aegis'),
    ('UNITED', 'United'),
    ('SOLITARY', 'Solitary'),
    ('COBALT', 'Cobalt'),
    ('OMEGA', 'Omega'),
    ('ECHO', 'Echo'),
    ('LORDS', 'Lords'),
    ('CULT', 'Cult'),
    ('ANCIENTS', 'Ancients'),
    ('SHADOW', 'Shadow'),
    ('ETHEREAL', 'Ethereal')
]

FACTION_TRAIT_SYMBOLS = [
    ('BUREAUCRATIC', 'Bureaucratic'),
    ('SECRETIVE', 'Secretive'),
    ('CAPITALISTIC', 'Capitalistic'),
    ('INDUSTRIOUS', 'Industrious'),
    ('PEACEFUL', 'Peaceful'),
    ('DISTRUSTFUL', 'Distrustful'),
    ('WELCOMING', 'Welcoming'),
    ('SMUGGLERS', 'Smugglers'),
    ('SCAVENGERS', 'Scavengers'),
    ('REBELLIOUS', 'Rebellious'),
    ('EXILES', 'Exiles'),
    ('PIRATES', 'Pirates'),
    ('RAIDERS', 'Raiders'),
    ('CLAN', 'Clan'),
    ('GUILD', 'Guild'),
    ('DOMINION', 'Dominion'),
    ('FRINGE', 'Fringe'),
    ('FORSAKEN', 'Forsaken'),
    ('ISOLATED', 'Isolated'),
    ('LOCALIZED', 'Localized'),
    ('ESTABLISHED', 'Established'),
    ('NOTABLE', 'Notable'),
    ('DOMINANT', 'Dominant'),
    ('INESCAPABLE', 'Inescapable'),
    ('INNOVATIVE', 'Innovative'),
    ('BOLD', 'Bold'),
    ('VISIONARY', 'Visionary'),
    ('CURIOUS', 'Curious'),
    ('DARING', 'Daring'),
    ('EXPLORATORY', 'Exploratory'),
    ('RESOURCEFUL', 'Resourceful'),
    ('FLEXIBLE', 'Flexible'),
    ('COOPERATIVE', 'Cooperative'),
    ('UNITED', 'United'),
    ('STRATEGIC', 'Strategic'),
    ('INTELLIGENT', 'Intelligent'),
    ('RESEARCH_FOCUSED', 'Research_Focused'),
    ('COLLABORATIVE', 'Collaborative'),
    ('PROGRESSIVE', 'Progressive'),
    ('MILITARISTIC', 'Militaristic'),
    ('TECHNOLOGICALLY_ADVANCED', 'Technologically Advanced'),
    ('AGGRESSIVE', 'Aggressive'),
    ('IMPERIALISTIC', 'Imperialistic'),
    ('TREASURE_HUNTERS', 'Treasure_Hunters'),
    ('DEXTEROUS', 'Dexterous'),
    ('UNPREDICTABLE', 'Unpredictable'),
    ('BRUTAL', 'Brutal'),
    ('FLEETING', 'Fleeting'),
    ('ADAPTABLE', 'Adaptable'),
    ('SELF_SUFFICIENT', 'Self Sufficient'),
    ('DEFENSIVE', 'Defensive'),
    ('PROUD', 'Proud'),
    ('DIVERSE', 'Diverse'),
    ('INDEPENDENT', 'Independent'),
    ('SELF_INTERESTED', 'Self Interested'),
    ('FRAGMENTED', 'Fragmented'),
    ('COMMERCIAL', 'Commercial'),
    ('FREE_MARKETS', 'Free Markets'),
    ('ENTREPRENEURIAL', 'Entrepreneurial')
]


class Faction(models.Model):
    symbol = models.CharField(
        primary_key=True,
        max_length=500,
        choices=FACTION_SYMBOLS
    )
    name = models.CharField(
        max_length=500
    )
    description = models.CharField(
        max_length=5000
    )
    headquarters = models.ForeignKey(
        'systems.System',
        on_delete=models.CASCADE,
        related_name='faction_headquarters',
        null=True
    )
    is_recruiting = models.BooleanField()
    traits = models.ManyToManyField(
        'FactionTrait',
        through='FactionTraitLink',
        related_name='factions'
    )

    def __str__(self):
        if self.headquarters is None:
            return "faction is not finished initializing yet"
        return f'{self.name}, headquarters at {self.headquarters.symbol}. They are{" not " if self.is_recruiting is False else " "}recruiting.'
    
    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def add_faction_no_waypoint(cls, faction_data):
        faction, created = cls.objects.update_or_create(
            symbol=faction_data['symbol'],
            name=faction_data['name'],
            description=faction_data['description'],
            headquarters=None,
            is_recruiting=faction_data['isRecruiting']
        )
        for trait in faction_data.get('traits'):
            if trait:
                faction_trait = FactionTrait.add(trait)
                FactionTraitLink.add(faction, faction_trait)
            else:
                continue
        return faction


class FactionTrait(models.Model):
    symbol = models.CharField(
        primary_key=True,
        max_length=500,
        choices=FACTION_TRAIT_SYMBOLS
    )
    name = models.CharField(
        max_length=500
    )
    description = models.CharField(
        max_length=5000
    )

    def __str__(self):
        return f'{self.name}: {self.description}'

    @classmethod
    def add(cls, faction_trait_data):
        faction_trait, created = cls.objects.update_or_create(
            symbol=faction_trait_data['symbol'],
            name=faction_trait_data['name'],
            description=faction_trait_data['description']
        )
        return faction_trait



# TODO decide if I simply let Django create this table by not using 'through' in the ManyToManyField
class FactionTraitLink(models.Model):
    faction = models.ForeignKey(
        Faction,
        on_delete=models.CASCADE,
    )
    faction_trait = models.ForeignKey(
        FactionTrait,
        on_delete=models.CASCADE,
    )

    @classmethod
    def add(cls, faction, faction_trait):
        faction_trait_link, created = cls.objects.update_or_create(
            faction=faction,
            faction_trait=faction_trait
        )
        faction_trait_link.save()
        return faction_trait_link
