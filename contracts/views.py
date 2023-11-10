from django.shortcuts import redirect
from django.views import generic
from django.contrib import messages

from .models import Contract
from player.api import SpaceTradersAPI
from factions.models import Faction
from agents.models import Agent
from systems.models import Waypoint


class IndexView(generic.ListView):
    template_name = 'contracts/index.html'
    context_object_name = 'contract_list'

    def get_queryset(self):
        return Contract.objects.all().order_by('accepted', 'deadline_to_accept')


class DetailView(generic.DetailView):
    model = Contract
    template_name = 'contracts/detail.html'

    def post(self, request, *args, **kwargs):
        if request.POST.get('accept'):
            print(f'Accepting contract {request.POST.get("contract_id")}...')
            api = SpaceTradersAPI(request.user.token)

            contract_accepted_data = api.contract_accept(contract_id=request.POST.get('contract_id'))
            faction = Faction.objects.get(symbol=contract_accepted_data['contract']['factionSymbol'])

            SpaceTradersAPI.get_add_system(contract_accepted_data['agent']['headquarters'])
            waypoint = Waypoint.objects.get(symbol=contract_accepted_data['agent']['headquarters'])
            Agent.add(contract_accepted_data['agent'], faction=faction, waypoint=waypoint)

            contract = Contract.add(contract_accepted_data['contract'], agent=request.user.agent, faction=faction)
            messages.success(request, f'Contract {contract} successfully accepted!')
            return redirect('contracts:detail', pk=contract.pk)
        elif request.POST.get('update'):
            print(f'Updating contract {request.POST.get("contract_id")}...')
            api = SpaceTradersAPI(request.user.token)
            contract = api.get_add_contract(request.POST.get('contract_id'))
            messages.success(request, f'Contract {contract} successfully updated!')
            return redirect('contracts:detail', pk=contract.pk)
        return super().get(request, *args, **kwargs)
