from typing import Any
from django import forms
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from .models import System, Waypoint, Market, JumpGate
from player.api import SpaceTradersAPI
from fleet.models import Shipyard, ShipyardShip, Ship, ShipyardShipLink


class IndexView(generic.ListView):
    template_name = 'systems/index.html'
    context_object_name = 'system_list'

    def get_queryset(self):
        return System.objects.all()


class DetailView(generic.DetailView):
    model = System
    template_name = 'systems/detail.html'

    def post(self, request, *args, **kwargs):
        if request.POST.get('update_system'):
            print(f'Updating system {request.POST.get("system_symbol")}...')
            system = SpaceTradersAPI.system_deep_get(request.POST.get('system_symbol'))
            messages.success(request, f'System {system} successfully updated!')
            return redirect('systems:detail', pk=system.pk)


class WaypointIndexView(generic.ListView):
    template_name = 'systems/waypoint_index.html'
    context_object_name = 'waypoint_list'


    def get_queryset(self):
        return Waypoint.objects.filter(system__symbol=self.kwargs['system_symbol']).order_by('waypoint_type')


class WaypointDetailView(generic.DetailView):
    model = Waypoint
    template_name = 'systems/waypoint_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fleet'] = Ship.objects.filter(agent=self.request.user.agent.pk).all()
        context['docked_ships'] = [ship for ship in context['fleet'] if ship.nav.waypoint.symbol == self.get_object().symbol and ship.nav.status == 'DOCKED']
        context['orbiting_ships'] = [ship for ship in context['fleet'] if ship.nav.waypoint.symbol == self.get_object().symbol and ship.nav.status == 'IN_ORBIT']
        return context

    def post(self, request, *args, **kwargs):
        waypoint = self.get_object()

        if request.POST.get('update_waypoint'):
            print(f'Updating waypoint {waypoint.symbol}...')
            waypoint = SpaceTradersAPI.update_waypoint(waypoint.symbol)
            messages.success(request, f'Waypoint {waypoint} successfully updated!')
            return redirect('systems:waypoint_detail', system_symbol=waypoint.system.symbol, pk=waypoint.pk)
        
        if request.POST.get('navigate'):
            ship = Ship.objects.get(symbol=request.POST.get("ship_symbol"))
            print(f'Navigating {ship} to {waypoint.symbol}...')
            api = SpaceTradersAPI(request.user.token)
            if ship.nav.status == 'DOCKED':
                api.orbit_ship(ship.symbol)
            ship_nav = api.navigate_ship(ship.symbol, waypoint.symbol)
            return redirect('fleet:nav', pk=ship_nav.ship.symbol)
        
        if request.POST.get('refuel'):
            ship = Ship.objects.get(symbol=request.POST.get("ship_symbol"))
            print(f'Refuelling {ship} at {waypoint.symbol}...')
            api = SpaceTradersAPI(request.user.token)
            market_transaction = api.refuel_ship(ship.symbol)
            messages.success(request, f'{market_transaction}')
            return redirect('fleet:detail', pk=ship.symbol)
        
        if request.POST.get('extract'):
            ship = Ship.objects.get(symbol=request.POST.get("ship_symbol"))
            print(f'{ship} is extracting at {waypoint.symbol}...')
            api = SpaceTradersAPI(request.user.token)
            cooldown, inventory = api.ship_extract_resources(ship.symbol)
            messages.success(request, f'{ship} is on cooldown for {cooldown.remaining_seconds} s')
            messages.success(request, f'{ship} current inventory:')
            for item in inventory:
                print(item)
                messages.success(request, f'\t{item.units} {item.trade_good}')
            return redirect('systems:waypoint_detail', system_symbol=waypoint.system.symbol, pk=waypoint.pk)

        return super().get(request, *args, **kwargs)

class MarketDetailView(generic.DetailView):
    model = Market
    template_name = 'systems/market_detail.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['docked_ships'] = [ship for ship in Ship.objects.filter(agent=self.request.user.agent.pk).all() if ship.nav.waypoint.symbol == self.get_object().waypoint.symbol and ship.nav.status == 'DOCKED']
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('update_market'):
            print(f'Updating market {request.POST.get("market_symbol")}...')
            if request.user.is_authenticated:
                api = SpaceTradersAPI(request.user.token)
                market = api.get_add_market(request.POST.get('market_symbol'))
            else:
                market = SpaceTradersAPI.get_add_market_no_token(request.POST.get('market_symbol'))
            messages.success(request, f'Market {market} successfully updated!')
            return redirect('systems:market_detail', system_symbol=market.waypoint.system.symbol, pk=market.pk)

        return super().get(request, *args, **kwargs)


class ShipyardDetailView(generic.DetailView):
    model = Shipyard
    template_name = 'systems/shipyard_detail.html'

    def post(self, request, *args, **kwargs):
        if request.POST.get('update_shipyard'):
            print(f'Updating shipyard {request.POST.get("shipyard_symbol")}...')
            if request.user.is_authenticated:
                api = SpaceTradersAPI(request.user.token)
                shipyard = api.get_add_shipyard(request.POST.get('shipyard_symbol'))
            else:
                shipyard = SpaceTradersAPI.get_add_shipyard_no_token(request.POST.get('shipyard_symbol'))
            messages.success(request, f'Shipyard {shipyard} successfully updated!')
            return redirect('systems:shipyard_detail', system_symbol=shipyard.waypoint.system.symbol, pk=shipyard.pk)
        return super().get(request, *args, **kwargs)


class ShipyardShipDetailView(generic.DetailView):
    model = ShipyardShip
    template_name = 'systems/shipyard_ship_detail.html'

    def get_object(self):
        return get_object_or_404(ShipyardShip, pk=self.kwargs['ship_id'])
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('buy'):
            print(f'Buying {self.get_object()}...')
            api = SpaceTradersAPI(request.user.token)
            # get the waypoint symbol from the url
            ship = api.purchase_ship(self.kwargs['pk'], self.get_object().ship_type)
            return redirect('fleet:detail', pk=ship.pk)
        return super().get(request, *args, **kwargs)