from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic


from .api import SpaceTradersAPI

from .models import Player
from systems.models import Market

class HomeView(generic.ListView):
    model = Player
    template_name = 'player/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['player'] = self.request.user
        return context
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('public_agent_symbol'):
            print(f'Adding agent {request.POST.get("public_agent_symbol")} to the database...')
            agent = SpaceTradersAPI.get_add_public_agent(
                request.POST.get('public_agent_symbol')
            )
            messages.success(request, f'Agent {agent.symbol} successfully added to the database!')
            return redirect('agents:detail', pk=agent.symbol)
        elif request.POST.get('contract_id'):
            contract_id = request.POST.get("contract_id")
            print(f'Adding contract {contract_id} to the database...')
            api = SpaceTradersAPI(request.user.token)
            contract = api.get_add_contract(contract_id)
            messages.success(request, f'Contract {contract} successfully added to the database!')
            return redirect('contracts:detail', pk=contract.contract_id)
        elif request.POST.get('update_contracts'):
            print(f'Updating contracts...')
            api = SpaceTradersAPI(request.user.token)
            contracts = api.get_add_all_contracts()
            messages.success(request, f'Updated {len(contracts)} contracts!')
            return redirect('contracts:index')
        elif request.POST.get('update_fleet'):
            print(f"Updating {request.user.agent.symbol}'s fleet...")
            api = SpaceTradersAPI(request.user.token)
            fleet = api.get_add_fleet()
            messages.success(request, f'Updated {len(fleet)} ships in {request.user.agent.symbol}\'s fleet!')
            return redirect('fleet:index')
        return super().get(request, *args, **kwargs)
    

class MarketIndexView(generic.ListView):
    template_name = 'player/market_index.html'
    context_object_name = 'market_list'

    def get_queryset(self):
        return Market.objects.all().order_by('pk')

