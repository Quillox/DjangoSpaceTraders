import requests
from time import sleep

from factions.models import Faction, FACTION_SYMBOLS
from systems.models import MarketTransaction, System, TradeGood, Waypoint, Chart, Market, JumpGate, ConstructionSite
from agents.models import Agent
from contracts.models import Contract
from fleet.models import Ship, ShipRegistration, ShipNav, ShipNavRoute, ShipCrew, Frame, Reactor, Engine, Module, Mount, Shipyard, ShipyardTransaction, FuelConsumedLog, Cooldown, ShipCargoInventory, Survey, Deposit
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
        if response.status_code in [200, 201]:
            return response.json()
        else:
            print(response.status_code)
            print(response.text)
            return None

    def patch_token(self, endpoint, payload=None):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_token}"
        }
        response = requests.patch(
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
    def get_add_system(cls, system_symbol, add_jump_gates=False):
        system_symbol = get_sector_system_waypoint(system_symbol)['system']
        if System.objects.filter(pk=system_symbol).exists():
            # TODO might need to remove this 
            return System.objects.get(symbol=system_symbol)
        sleep(0.5)
        system_data = cls.get_no_token(f'systems/{system_symbol}')['data']
        system = System.add(system_data)
        for waypoint_data in system_data['waypoints']:
            cls.add_waypoint(system_symbol, add_jump_gates, system_data, waypoint_data)

        return system
    
    @classmethod
    def system_deep_get(cls, system_symbol, add_jump_gates=True):
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
                    cls.get_add_market_no_token(waypoint.symbol)
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
    def update_waypoint(cls, waypoint_symbol):
        system_symbol = get_sector_system_waypoint(waypoint_symbol)['system']
        waypoint_data = cls.get_no_token(f'systems/{system_symbol}/waypoints/{waypoint_symbol}')['data']
        waypoint = Waypoint.objects.get(symbol=waypoint_symbol)
        waypoint.update(waypoint_data)

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
                    cls.get_add_market_no_token(waypoint.symbol)
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
            cls.get_add_market_no_token(waypoint_symbol)
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
    def get_add_market_no_token(cls, market_symbol):
        system_symbol = get_sector_system_waypoint(market_symbol)['system']
        market_data = cls.get_no_token(f'systems/{system_symbol}/waypoints/{market_symbol}/market')['data']
        market = Market.add(market_data)
        return market

    def get_add_market(self, market_symbol):
        system_symbol = get_sector_system_waypoint(market_symbol)['system']
        market_data = self.get_token(f'systems/{system_symbol}/waypoints/{market_symbol}/market')['data']
        market = Market.add(market_data)
        return market
    
    def get_ship_cargo(self, ship_symbol):
        ship_cargo_data = self.get_token(f'my/ships/{ship_symbol}/cargo')['data']
        ship = Ship.objects.get(symbol=ship_symbol)
        ship.cargo_capacity = ship_cargo_data['capacity']
        ship.cargo_units = ship_cargo_data['units']
        ship.save()
        ship_cargo_inventory = ShipCargoInventory.add(ship_cargo_data['inventory'], ship)
        return ship_cargo_inventory
    
    def sell_ship_cargo(self, ship_symbol, trade_good_symbol, units):
        payload = {
            'symbol': trade_good_symbol,
            'units': units
        }
        response_data = self.post_token(f'my/ships/{ship_symbol}/sell', payload)['data']
        agent = self.agent.add(
            response_data['agent'],
            Waypoint.objects.get(symbol=response_data['agent']['headquarters']),
            Faction.objects.get(symbol=response_data['agent']['startingFaction'])
        )
        ship = Ship.objects.get(symbol=ship_symbol)
        ship.cargo_capacity = response_data['cargo']['capacity']
        ship.cargo_units = response_data['cargo']['units']
        ship.save()
        ship_cargo_inventory = ShipCargoInventory.add(response_data['cargo']['inventory'], ship)
        market_transaction = MarketTransaction.add(
            response_data['transaction'],
            Market.objects.get(pk=response_data['transaction']['waypointSymbol']),
            ship,
            TradeGood.objects.get(symbol=response_data['transaction']['tradeSymbol'])
        )
        return market_transaction
    
    def contract_deliver_cargo(self, contract_id, ship_symbol, trade_good_symbol, units):
        payload = {
            'tradeSymbol': trade_good_symbol,
            'shipSymbol': ship_symbol,
            'units': units
        }
        response_data = self.post_token(f'my/contracts/{contract_id}/deliver', payload)['data']
        ship = Ship.objects.get(symbol=ship_symbol)
        ship.cargo_capacity = response_data['cargo']['capacity']
        ship.cargo_units = response_data['cargo']['units']
        ship.save()
        ship_cargo_inventory = ShipCargoInventory.add(response_data['cargo']['inventory'], ship)
        contract = Contract.add(
            response_data['contract'],
            self.agent,
            Faction.objects.get(symbol=response_data['contract']['factionSymbol'])
        )   
        return contract

    def fulfill_contract(self, contract_id):
        """Fulfill a contract. Can only be used on contracts that have all of their delivery terms fulfilled."""
        response_data = self.post_token(f'my/contracts/{contract_id}/fulfill')['data']
        agent = self.agent.add(
            response_data['agent'],
            Waypoint.objects.get(symbol=response_data['agent']['headquarters']),
            Faction.objects.get(symbol=response_data['agent']['startingFaction'])
        )
        contract = Contract.add(
            response_data['contract'],
            self.agent,
            Faction.objects.get(symbol=response_data['contract']['factionSymbol'])
        )
        return contract

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
    
    def get_add_shipyard(self, shipyard_symbol):
        system_symbol = get_sector_system_waypoint(shipyard_symbol)['system']
        shipyard_data = self.get_token(f'systems/{system_symbol}/waypoints/{shipyard_symbol}/shipyard')
        if not shipyard_data:
            print(f'Error: {shipyard_symbol} is not scannable!')
            return None
        else:
            shipyard_data = shipyard_data['data']
        # TODO I technically should not need to update the system here. But this is safe.
        # self.get_add_system(system_symbol)
        waypoint = Waypoint.objects.get(symbol=shipyard_symbol)
        shipyard = Shipyard.add(shipyard_data, waypoint)
        if shipyard_data.get('transactions'):
            for transaction_data in shipyard_data['transactions']:
                buyer = self.get_add_public_agent(transaction_data['agentSymbol'])
                shipyard_transaction = ShipyardTransaction.add(transaction_data, shipyard, buyer)
        return shipyard

    def purchase_ship(self, shipyard_symbol, ship_type):
        payload = {
            'shipType': ship_type,
            'waypointSymbol': shipyard_symbol
        }
        response_data = self.post_token(f'my/ships', payload)['data']
        ship = self.add_ship(response_data['ship'], self.agent)
        shipyard = Shipyard.objects.get(pk=shipyard_symbol)
        agent_headquarters = Waypoint.objects.get(symbol=response_data['agent']['headquarters'])
        agent_faction = Faction.objects.get(symbol=response_data['agent']['startingFaction'])
        self.agent.add(response_data['agent'], agent_headquarters, agent_faction)
        transaction = ShipyardTransaction.add(response_data['transaction'], shipyard, self.agent)
        return ship
    
    def orbit_ship(self, ship_symbol):
        response_data = self.post_token(f'my/ships/{ship_symbol}/orbit')['data']
        ship_nav = ShipNav.add(
            response_data['nav'],
            Ship.objects.get(pk=ship_symbol),
            System.objects.get(symbol=response_data['nav']['systemSymbol']),
            Waypoint.objects.get(symbol=response_data['nav']['waypointSymbol'])
        )
        return ship_nav
    
    def dock_ship(self, ship_symbol):
        response_data = self.post_token(f'my/ships/{ship_symbol}/dock')['data']
        ship_nav = ShipNav.add(
            response_data['nav'],
            Ship.objects.get(pk=ship_symbol),
            System.objects.get(symbol=response_data['nav']['systemSymbol']),
            Waypoint.objects.get(symbol=response_data['nav']['waypointSymbol'])
        )
        return ship_nav
    
    def navigate_ship(self, ship_symbol, destination_symbol):
        payload = {
            'waypointSymbol': destination_symbol
        }
        response_data = self.post_token(f'my/ships/{ship_symbol}/navigate', payload)['data']
        ship_nav = ShipNav.add(
            response_data['nav'],
            Ship.objects.get(pk=ship_symbol),
            System.objects.get(symbol=response_data['nav']['systemSymbol']),
            Waypoint.objects.get(symbol=response_data['nav']['waypointSymbol'])
        )
        ship = Ship.objects.get(symbol=ship_symbol)
        ship.fuel_current = response_data['fuel']['current']
        ship.fuel_capacity = response_data['fuel']['capacity']
        ship.save()
        fuel_log = FuelConsumedLog.add(response_data['fuel']['consumed'], ship)
        return ship_nav
    
    def refuel_ship(self, ship_symbol, units: str=None):
        if units:
            payload = {
                'units': units
            }
        response_data = self.post_token(f'my/ships/{ship_symbol}/refuel')['data']
        self.agent.add(
            response_data['agent'],
            Waypoint.objects.get(symbol=response_data['agent']['headquarters']),
            Faction.objects.get(symbol=response_data['agent']['startingFaction'])
        )
        ship = Ship.objects.get(pk=ship_symbol)
        ship.fuel_current = response_data['fuel']['current']
        ship.fuel_capacity = response_data['fuel']['capacity']
        ship.save()
        fuel_log = FuelConsumedLog.add(response_data['fuel']['consumed'], ship)
        market_transaction = MarketTransaction.add(
            response_data['transaction'],
            Market.objects.get(pk=response_data['transaction']['waypointSymbol']),
            ship,
            TradeGood.objects.get(symbol=response_data['transaction']['tradeSymbol'])
        )
        return market_transaction
    
    def ship_extract_resources(self, ship_symbol, survey_signature=None):
        if survey_signature:
            payload = Survey.objects.get(pk=survey_signature).get_json()
            extraction_data = self.post_token(f'my/ships/{ship_symbol}/extract', payload)['data']
        else:
            extraction_data = self.post_token(f'my/ships/{ship_symbol}/extract')['data']
        ship = Ship.objects.get(pk=ship_symbol)
        ship.cargo_capacity = extraction_data['cargo']['capacity']
        ship.cargo_units = extraction_data['cargo']['units']
        cooldown = Cooldown.add(extraction_data['cooldown'], ship)
        ship_cargo_inventory = ShipCargoInventory.add(extraction_data['cargo']['inventory'], ship)
        return cooldown, ship_cargo_inventory
    
    def ship_jettison_cargo(self, ship_symbol, trade_good_symbol, units):
        payload = {
            'symbol': trade_good_symbol,
            'units': units
        }
        response_data = self.post_token(f'my/ships/{ship_symbol}/jettison', payload)['data']
        ship = Ship.objects.get(pk=ship_symbol)
        ship.cargo_capacity = response_data['cargo']['capacity']
        ship.cargo_units = response_data['cargo']['units']
        ship.save()
        ship_cargo_inventory = ShipCargoInventory.add(response_data['cargo']['inventory'], ship)
        return ship_cargo_inventory
    
    def purchase_ship_cargo(self, ship_symbol, trade_good_symbol, units):
        payload = {
            'symbol': trade_good_symbol,
            'units': units
        }
        response_data = self.post_token(f'my/ships/{ship_symbol}/purchase', payload)['data']
        ship = Ship.objects.get(pk=ship_symbol)
        ship.cargo_capacity = response_data['cargo']['capacity']
        ship.cargo_units = response_data['cargo']['units']
        ship.save()
        ship_cargo_inventory = ShipCargoInventory.add(response_data['cargo']['inventory'], ship)
        market_transaction = MarketTransaction.add(
            response_data['transaction'],
            Market.objects.get(pk=response_data['transaction']['waypointSymbol']),
            ship,
            TradeGood.objects.get(symbol=response_data['transaction']['tradeSymbol'])
        )
        return market_transaction

    def ship_survey(self, ship_symbol):
        response_data = self.post_token(f'my/ships/{ship_symbol}/survey')['data']
        cooldown = Cooldown.add(response_data['cooldown'], Ship.objects.get(pk=ship_symbol))
        for survey_data in response_data['surveys']:
            survey = Survey.add(
                survey_data,
                Waypoint.objects.get(symbol=survey_data['symbol'])
            )
            for deposit_data in survey_data['deposits']:
                trade_good = TradeGood.objects.get(symbol=deposit_data['symbol'])
                deposit = Deposit.add(survey, trade_good)
        return cooldown, survey
    
    def patch_ship_nav(self, ship_symbol, flight_mode):
        payload = {
            'flightMode': flight_mode
        }
        response_data = self.patch_token(f'my/ships/{ship_symbol}/nav', payload)['data']
        ship_nav = ShipNav.add(
            response_data,
            Ship.objects.get(pk=ship_symbol),
            System.objects.get(symbol=response_data['systemSymbol']),
            Waypoint.objects.get(symbol=response_data['waypointSymbol'])
        )
        return ship_nav

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
                cls.get_add_system(headquarters_system_symbol, add_jump_gates=False)
                headquarters = System.objects.get(symbol=headquarters_symbol)
                faction.headquarters = headquarters
                faction.save()
                print(f'Updated {faction.symbol} headquarters: {headquarters_symbol}')


        print('Factions successfully populated!')

