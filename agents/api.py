import requests
from time import sleep

from factions.models import Faction, FACTION_SYMBOLS
from systems.models import System, TradeGood, Waypoint, Chart
from .models import Agent
from contracts.models import Contract


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
        self.api_status = self.check_api_status()

    def check_api_status(self):
        api_status = self.get_token('')
        if api_status is None:
            response_no_auth = requests.get(self.base_url)
            if response_no_auth.status_code == 200:
                print('API is up!')
                print('Invalid API token!')
                return 'Invalid API token!'
            else:
                print('API is down!')
                return 'Offline'
        else:
            print('API is up!')
            print('Valid API token!')
            return 'Online'

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

    def post_token(self, endpoint, payload):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
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
        api = cls(token)
        if api.check_api_status() == 'Invalid API token!':
            return False
        else:
            return True

    @classmethod
    def get_add_system(cls, system_symbol):
        system_symbol = get_sector_system_waypoint(system_symbol)['system']
        system_data = cls.get_no_token(f'systems/{system_symbol}')['data']
        system = System.add(system_data)
        for waypoint_data in system_data['waypoints']:
            waypoint_symbol = waypoint_data['symbol']
            if Waypoint.objects.filter(symbol=waypoint_symbol).exists():
                continue
            cls._get_add_waypoint(waypoint_symbol)
            sleep(0.5)
        return system

    @classmethod
    def _get_add_waypoint(cls, waypoint_symbol, add_chart=True):
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

        if waypoint_data.get('chart').get('submittedBy') and add_chart:
            waypoint = Waypoint.add(waypoint_data)

            agent_symbol = waypoint_data['chart']['submittedBy']
            if agent_symbol in [symbol for symbol, _ in FACTION_SYMBOLS]:
                chart_agent = Agent.objects.get(symbol=f'{agent_symbol}-agent')
            else:
                chart_agent = cls.get_add_public_agent(waypoint_data['chart']['submittedBy'])
            Chart.add(waypoint, chart_agent, waypoint_data['chart']['submittedOn'])
            return waypoint

        return Waypoint.add(waypoint_data)

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
        headquarters = agent_data['headquarters']
        self.get_add_system(headquarters)
        waypoint = Waypoint.objects.get(symbol=headquarters)
        faction = Faction.objects.get(symbol=agent_data['startingFaction'])
        return Agent.add(agent_data, waypoint, faction)
    
    def get_add_contract(self, contract_id):
        contract_data = self.get_token(f'my/contracts/{contract_id}')['data']
        faction = Faction.objects.get(symbol=contract_data['factionSymbol'])
        SpaceTradersAPI.get_add_system(contract_data['terms']['deliver']['destinationSymbol'])
        waypoint = Waypoint.objects.get(symbol=contract_data['terms']['deliver']['destinationSymbol'])
        trade_good = TradeGood.add({'symbol':contract_data['terms']['deliver']['tradeSymbol']})
        contract = Contract.add(contract_data, faction, waypoint, trade_good)
        return contract


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
            Agent.add(faction_agent_data)

        # Now add the waypoints to the factions
        for faction_data in response.json()['data']:
            faction = Faction.objects.get(symbol=faction_data['symbol'])

            if faction_data.get('headquarters'):
                headquarters_symbol = faction_data['headquarters']
                headquarters_system_symbol = get_sector_system_waypoint(headquarters_symbol)['system']
                cls.get_add_system(headquarters_system_symbol)
                print(f'####### Adding {faction.symbol} headquarters: {headquarters_symbol}')
                headquarters = System.objects.get(symbol=headquarters_symbol)
                faction.headquarters = headquarters
                faction.save()


        print('Factions successfully populated!')
