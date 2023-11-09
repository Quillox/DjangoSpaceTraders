import requests
from time import sleep

from factions.models import Faction, FACTION_SYMBOLS
from systems.models import System, TradeGood, Waypoint, Chart, Market, JumpGate, ConstructionSite
from agents.models import Agent
from contracts.models import Contract
from fleet.models import Ship, ShipRegistration, ShipNav, ShipNavRoute, ShipCrew, Frame, Reactor, Engine, Module, Mount, Shipyard
from player.models import Player


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


class SpaceTradersAPI:
    base_url = 'https://api.spacetraders.io/v2'

    def __init__(self, api_token):
        self.api_token = api_token
        self.agent = Player.objects.get(token=api_token).agent

    def get_token(self, endpoint):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_token}"
        }
        response = requests.get(f'{self.base_url}/{endpoint}', headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error: {response.status_code}: {response.text}')
            return None

    def post_token(self, endpoint, payload=None):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_token}"
        }
        response = requests.post(
            f'{self.base_url}/{endpoint}', headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            print(response.text)
            return None

    @classmethod
    def get_no_token(cls, endpoint):
        headers = {"Accept": "application/json"}
        response = requests.get(f'{cls.base_url}/{endpoint}', headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error: {response.status_code}: {response.text}')
            print('The request was:')
            print(f'\t{cls.base_url}/{endpoint}')
            return None

    @classmethod
    def validate_token(cls, token):
        response_no_auth = requests.get(cls.base_url)
        if response_no_auth.status_code != 200:
            print('API is down!')
            return False
        else:
            response = requests.get(f'{cls.base_url}/my/account', headers={"Authorization": f"Bearer {token}"})
            if response.status_code != 200:
                print('Invalid API token!')
                return False
            else:
                print('Valid API token!')
                return True

    @classmethod
    def get_add_system(cls, system_symbol, add_jump_gates=True):
        sleep(0.5)
        system_symbol = get_sector_system_waypoint(system_symbol)['system']
        system_data = cls.get_no_token(f'systems/{system_symbol}')['data']
        system = System.add(system_data)
        for waypoint_data in system_data['waypoints']:
            cls.add_waypoint(system_symbol, add_jump_gates, system_data, waypoint_data)

        return system
    
    @classmethod
    def system_deep_get(cls, system_symbol, add_jump_gates=False):
        system_symbol = get_sector_system_waypoint(system_symbol)['system']
        system_data = cls.get_no_token(f'systems/{system_symbol}')['data']
        system = System.add(system_data)
        for waypoint_data_shallow in system_data['waypoints']:
            sleep(0.5)
            waypoint_data_deep = cls.get_no_token(f'systems/{system_symbol}/waypoints/{waypoint_data_shallow["symbol"]}')
            if waypoint_data_deep:
                waypoint_data_deep = waypoint_data_deep['data']
                cls.add_waypoint(system_symbol, add_jump_gates, system_data, waypoint_data_deep)
            else:
                print(f'Waypoint {waypoint_data_shallow["symbol"]} not accessible!')
        return system


    @classmethod
    def add_waypoint(cls, system_symbol, add_jump_gates, system_data, waypoint_data):
        if waypoint_data.get('orbits'):
            parent_waypoint_symbol = waypoint_data['orbits']
            parent_waypoint_data = next((waypoint for waypoint in system_data['waypoints'] if waypoint['symbol'] == parent_waypoint_symbol), None)
            if parent_waypoint_data:
                Waypoint.add(parent_waypoint_data)

        waypoint = Waypoint.add(waypoint_data)
            
        if add_jump_gates:
            if waypoint.waypoint_type == 'JUMP_GATE':
                if cls.get_no_token(f'systems/{system_symbol}/waypoints/{waypoint.symbol}/jump-gate'):
                    cls.get_add_jump_gate(waypoint.symbol)
        
        if waypoint.is_under_construction:
            construction_site_data = cls.get_no_token(f'systems/{system_symbol}/waypoints/{waypoint.symbol}/construction')
            if construction_site_data:
                construction_site_data = construction_site_data['data']
                for material in construction_site_data['materials']:
                    trade_good = TradeGood.add({'symbol':material['tradeSymbol'], 'name':None, 'description':None})
                    required = material['required']
                    fulfilled = material['fulfilled']
                    ConstructionSite.add(waypoint, trade_good, required, fulfilled)
                waypoint.is_under_construction = construction_site_data['isComplete']
                waypoint.save()

        if waypoint_data.get('traits'):
            waypoint_traits = [trait_data['symbol'] for trait_data in waypoint_data['traits']]
            # TODO decide where to put handling of the api request answer being None
            if 'MARKETPLACE' in waypoint_traits:
                if cls.get_no_token(f'systems/{system_symbol}/waypoints/{waypoint.symbol}/market'):
                    cls.get_add_market(waypoint.symbol)
            if 'SHIPYARD' in waypoint_traits:
                cls.get_add_shipyard_no_token(waypoint.symbol)

        if waypoint_data.get('chart'):
            agent_symbol = waypoint_data['chart']['submittedBy']
            if agent_symbol in [symbol for symbol, _ in FACTION_SYMBOLS]:
                chart_agent = Agent.objects.get(symbol=f'{agent_symbol}-agent')
            else:
                chart_agent = cls.get_add_public_agent(waypoint_data['chart']['submittedBy'])
            Chart.add(waypoint, chart_agent, waypoint_data['chart']['submittedOn'])

        return waypoint

    @classmethod
    def _get_add_waypoint(cls, waypoint_symbol):
        """Adds waypoint to the database. Don't use this method directly, use get_add_system instead.

        Parameters
        ----------
        waypoint_symbol : str
            waypoint symbol
        add_chart : bool, optional
            Add chart, by default True

        Returns
        -------
        Waypoint
            The waypoint object
        """
        system_symbol = get_sector_system_waypoint(waypoint_symbol)['system']
        waypoint_data = cls.get_no_token(f'systems/{system_symbol}/waypoints/{waypoint_symbol}')['data']
        if waypoint_data.get('orbits'):
            parent_waypoint_data = cls.get_no_token(f'systems/{system_symbol}/waypoints/{waypoint_data["orbits"]}')['data']
            cls._get_add_waypoint(parent_waypoint_data['symbol'])


        waypoint = Waypoint.add(waypoint_data)

        if waypoint.waypoint_type == 'JUMP_GATE':
            cls.get_add_jump_gate(waypoint_symbol)

        if 'MARKETPLACE' in [trait_data['symbol'] for trait_data in waypoint_data['traits']]:
            cls.get_add_market(waypoint_symbol)
        if 'SHIPYARD' in [trait_data['symbol'] for trait_data in waypoint_data['traits']]:
            pass
            

        if waypoint_data.get('chart'):
            agent_symbol = waypoint_data['chart']['submittedBy']
            if agent_symbol in [symbol for symbol, _ in FACTION_SYMBOLS]:
                chart_agent = Agent.objects.get(symbol=f'{agent_symbol}-agent')
            else:
                chart_agent = cls.get_add_public_agent(waypoint_data['chart']['submittedBy'])
            Chart.add(waypoint, chart_agent, waypoint_data['chart']['submittedOn'])
        return waypoint

    @classmethod
    def get_add_public_agent(cls, agent_symbol):
        if agent_symbol in [symbol for symbol, _ in FACTION_SYMBOLS]:
            return Agent.objects.get(symbol=f'{agent_symbol}-agent')

        agent_data = cls.get_no_token(f'agents/{agent_symbol}')['data']
        headquarters = agent_data['headquarters']
        cls.get_add_system(headquarters)
        waypoint = Waypoint.objects.get(symbol=headquarters)
        faction = Faction.objects.get(symbol=agent_data['startingFaction'])
        return Agent.add(agent_data, waypoint, faction)

    def get_add_my_agent(self):
        agent_data = self.get_token('my/agent')['data']
        headquarters_symbol = agent_data['headquarters']
        self.get_add_system(headquarters_symbol)
        waypoint = Waypoint.objects.get(symbol=headquarters_symbol)
        faction = Faction.objects.get(symbol=agent_data['startingFaction'])
        return Agent.add(agent_data, waypoint, faction)

    def get_add_contract(self, contract_id):
        contract_data = self.get_token(f'my/contracts/{contract_id}')['data']
        contract = self.add_contract(contract_data)
        return contract

    def add_contract(self, contract_data):
        faction = Faction.objects.get(symbol=contract_data['factionSymbol'])
        for deliver_data in contract_data['terms']['deliver']:
            SpaceTradersAPI.get_add_system(deliver_data['destinationSymbol'])
            TradeGood.add({'symbol':deliver_data['tradeSymbol'], 'name':None, 'description':None})
        contract = Contract.add(contract_data, self.agent, faction)
        return contract

    def get_add_all_contracts(self):
        contracts_data = self.get_token('my/contracts')['data']
        for contract_data in contracts_data:
            self.add_contract(contract_data)
            return Contract.objects.filter(agent=self.agent)

    def contract_accept(self, contract_id):
        response = self.post_token(f'my/contracts/{contract_id}/accept', {})
        if response:
            return response['data']
        else:
            print(f'Error: contract {contract_id} not accepted!')
            return None

    def get_add_ship(self, ship_symbol):
        ship_data = self.get_token(f'my/ships/{ship_symbol}')['data']
        agent = self.agent

        ship = self.add_ship(ship_data, agent)

        return ship

    @classmethod
    def add_ship(cls, ship_data, agent):
        frame = Frame.add(ship_data['frame'])
        reactor = Reactor.add(ship_data['reactor'])
        engine = Engine.add(ship_data['engine'])
        modules = []
        for module_data in ship_data['modules']:
            modules.append(Module.add(module_data))
        mounts = []
        for mount_data in ship_data['mounts']:
            deposits = []
            if mount_data.get('deposits'):
                for trade_good_symbol in mount_data['deposits']:
                    deposits.append(TradeGood.add({'symbol':trade_good_symbol, 'name':None, 'description':None}))
            mounts.append(Mount.add(mount_data, deposits))

        ship = Ship.add(ship_data, agent, frame, reactor, engine, modules, mounts)

        faction = Faction.objects.get(symbol=ship_data['registration']['factionSymbol'])
        registration = ShipRegistration.add(ship_data['registration'], ship, agent, faction)

        nav_system = cls.get_add_system(ship_data['nav']['systemSymbol'])
        nav_waypoint = Waypoint.objects.get(symbol=ship_data['nav']['waypointSymbol'])
        nav = ShipNav.add(ship_data['nav'], ship, nav_system, nav_waypoint)
        route_destination = Waypoint.objects.get(symbol=ship_data['nav']['route']['destination']['symbol'])
        route_origin = Waypoint.objects.get(symbol=ship_data['nav']['route']['origin']['symbol'])
        route = ShipNavRoute.add(ship_data['nav']['route'], nav, route_destination, route_origin)

        crew = ShipCrew.add(ship_data['crew'], ship)
        return ship

    def get_add_fleet(self):
        fleet_data = self.get_token('my/ships')['data']
        agent = self.agent
        fleet = []
        for ship_data in fleet_data:
            fleet.append(self.add_ship(ship_data, agent))
        return fleet

    @classmethod
    def get_add_market(cls, market_symbol):
        system_symbol = get_sector_system_waypoint(market_symbol)['system']
        market_data = cls.get_no_token(f'systems/{system_symbol}/waypoints/{market_symbol}/market')['data']
        market = Market.add(market_data)
        return market

    @classmethod
    def get_add_jump_gate(cls, jump_gate_symbol):
        system_symbol = get_sector_system_waypoint(jump_gate_symbol)['system']
        waypoint = Waypoint.objects.get(symbol=jump_gate_symbol)
        jump_gate_data = cls.get_no_token(f'systems/{system_symbol}/waypoints/{jump_gate_symbol}/jump-gate')['data']
        for destination_symbol in jump_gate_data['connections']:
            print(f'Adding {destination_symbol} as {jump_gate_symbol} jump gate destination.')
            cls.get_add_system(destination_symbol, add_jump_gates=False)
            sleep(0.5)
            destination = Waypoint.objects.get(symbol=destination_symbol)
            jump_gate = JumpGate.add(waypoint, destination)
        return jump_gate

    @classmethod
    def get_add_shipyard_no_token(cls, shipyard_symbol):
        system_symbol = get_sector_system_waypoint(shipyard_symbol)['system']
        shipyard_data = cls.get_no_token(f'systems/{system_symbol}/waypoints/{shipyard_symbol}/shipyard')
        if not shipyard_data:
            print(f'Error: {shipyard_symbol} is not scannable!')
            return None
        cls.get_add_system(system_symbol)
        waypoint = Waypoint.objects.get(symbol=shipyard_symbol)
        shipyard = Shipyard.add(shipyard_data, waypoint)
        return shipyard


    @classmethod
    def populate_factions(cls):
        url = "https://api.spacetraders.io/v2/factions"
        querystring = {"limit": "20"}
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers, params=querystring)

        # First add all the factions (and their mock agents) without waypoints to the database
        for faction_data in response.json()['data']:
            faction = Faction.add_faction_no_waypoint(faction_data)

            faction_agent_data = {
                'symbol': f'{faction.symbol}-agent',
                'headquarters': None,
                'credits': 0,
                'startingFaction': faction,
                'shipCount': 0,
                'accountId': None
            }
            Agent.add(faction_agent_data, None, faction)
            print(f'Added {faction.symbol} with mock agent {faction.symbol}-agent to the database.')

        # Now add the system headquarters to the factions
        for faction_data in response.json()['data']:
            faction = Faction.objects.get(symbol=faction_data['symbol'])

            if faction_data.get('headquarters'):
                headquarters_symbol = faction_data['headquarters']
                headquarters_system_symbol = get_sector_system_waypoint(headquarters_symbol)['system']
                cls.get_add_system(headquarters_system_symbol)
                sleep(0.5)
                headquarters = System.objects.get(symbol=headquarters_symbol)
                faction.headquarters = headquarters
                faction.save()
                print(f'Updated {faction.symbol} headquarters: {headquarters_symbol}')


        print('Factions successfully populated!')

