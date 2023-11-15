from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from .models import Ship, ShipNav, ShipCargoInventory
from player.api import SpaceTradersAPI
from systems.models import Waypoint, Market, TradeGood
from contracts.models import Contract


class IndexView(generic.ListView):
    template_name = 'fleet/index.html'
    context_object_name = 'fleet_list'

    def get_queryset(self):
        return Ship.objects.filter(agent=self.request.user.agent.pk).all()

    def post(self, request, *args, **kwargs):
        if request.POST.get('update_fleet'):
            print(f"Updating {request.user.agent.symbol}'s fleet...")
            api = SpaceTradersAPI(request.user.token)
            fleet = api.get_add_fleet()
            messages.success(request, f'Updated {len(fleet)} ships in {request.user.agent.symbol}\'s fleet!')
            return redirect('fleet:index')
        return super().get(request, *args, **kwargs)


class DetailView(generic.DetailView):
    model = Ship
    template_name = 'fleet/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contracts'] = context['ship'].agent.contracts.all()
        context['market'] = context['ship'].nav.waypoint.market if context['ship'].nav.status == 'DOCKED' else None
        context['waypoint'] = context['ship'].nav.waypoint if context['ship'].nav.status in ['DOCKED', 'IN_ORBIT'] else None
        return context
    
    def post(self, request, *args, **kwargs):
        waypoint = self.get_object().nav.waypoint if self.get_object().nav.status in ['DOCKED', 'IN_ORBIT'] else None
        if request.POST.get('update'):
            print(f'Updating {self.get_object()}...')
            api = SpaceTradersAPI(request.user.token)
            ship = api.get_add_ship(self.get_object().symbol)
            return redirect('fleet:detail', pk=ship.symbol)
        
        if request.POST.get('survey'):
            print(f'Surveying {waypoint} with {self.get_object()}...')
            api = SpaceTradersAPI(request.user.token)
            cooldown, survey = api.ship_survey(self.get_object().symbol)
            messages.success(request, f'Surveyed {waypoint} with {self.get_object()}!')
            for survey in waypoint.surveys.all():
                if survey.is_valid():
                    messages.info(request, f'Surveys: {survey}')
            messages.info(request, f'Cooldown: {cooldown}')
            return redirect('fleet:detail', pk=self.get_object().symbol)


class NavView(generic.DetailView):
    model = ShipNav
    template_name = 'fleet/nav.html'

    def post(self, request, *args, **kwargs):
        if request.POST.get('orbit'):
            print(f'Orbiting {self.get_object()}...')
            api = SpaceTradersAPI(request.user.token)
            ship_nav = api.orbit_ship(self.get_object().ship.symbol)
            return redirect('fleet:nav', pk=ship_nav.ship.symbol)
        
        if request.POST.get('dock'):
            print(f'Docking {self.get_object()}...')
            api = SpaceTradersAPI(request.user.token)
            ship_nav = api.dock_ship(self.get_object().ship.symbol)
            return redirect('fleet:nav', pk=ship_nav.ship.symbol)
        
        if request.POST.get('update'):
            print(f'Updating nav for {self.get_object()}...')
            api = SpaceTradersAPI(request.user.token)
            ship = api.get_add_ship(self.get_object().ship.symbol)
            return redirect('fleet:nav', pk=ship.symbol)
        
        return super().get(request, *args, **kwargs)
        
        
class InventoryView(generic.ListView):
    template_name = 'fleet/inventory.html'
    context_object_name = 'inventory_list'

    def get_queryset(self):
        return ShipCargoInventory.objects.filter(ship=self.kwargs['pk']).all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ship'] = Ship.objects.get(symbol=self.kwargs['pk'])
        context['contracts'] = context['ship'].agent.contracts.all()
        context['market'] = context['ship'].nav.waypoint.market if context['ship'].nav.status == 'DOCKED' else None
        return context
    
    def post(self, request, *args, **kwargs):
        ship = Ship.objects.get(symbol=self.kwargs['pk'])
        if request.POST.get('update_inventory'):
            print(f'Updating inventory for {ship}...')
            api = SpaceTradersAPI(request.user.token)
            inventory = api.get_ship_cargo(ship.symbol)
            messages.success(request, f'Updated inventory for {ship}!')
            return redirect('fleet:inventory', pk=ship.symbol)

        if request.POST.get('sell_cargo'):
            ship = Ship.objects.get(symbol=request.POST.get("ship_symbol"))
            trade_good_symbol = request.POST.get("trade_good")
            trade_good = TradeGood.objects.get(symbol=trade_good_symbol)
            print(f'Selling {trade_good} from {ship} at {ship.nav.waypoint.market}...')
            api = SpaceTradersAPI(request.user.token)
            market_transaction = api.sell_ship_cargo(
                ship.symbol,
                trade_good_symbol,
                ship.cargo.get(trade_good=trade_good).units
            )
            messages.success(request, f'{market_transaction}')
            return redirect('fleet:inventory', pk=ship.symbol)
        
        if request.POST.get('purchase_cargo'):
            ship = Ship.objects.get(symbol=request.POST.get("ship_symbol"))
            trade_good_symbol = request.POST.get("trade_good")
            trade_good = TradeGood.objects.get(symbol=trade_good_symbol)
            print(f'Purchasing {trade_good} from {ship} at {ship.nav.waypoint.market}...')
            api = SpaceTradersAPI(request.user.token)
            market_transaction = api.purchase_ship_cargo(
                ship.symbol,
                trade_good_symbol,
                request.POST.get("units")
            )
            messages.success(request, f'{market_transaction}')
            return redirect('fleet:inventory', pk=ship.symbol)
        
        if request.POST.get('deliver_cargo'):
            # TODO make a proper form class for this
            ship = Ship.objects.get(symbol=request.POST.get("ship_symbol"))
            trade_good_symbol = request.POST.get("trade_good")
            trade_good = TradeGood.objects.get(symbol=trade_good_symbol)
            contract_id = Contract.objects.get(pk=request.POST.get("contract")).pk
            print(f'Delivering {trade_good} from {ship} at {ship.nav.waypoint}...')
            api = SpaceTradersAPI(request.user.token)
            contract = api.contract_deliver_cargo(
                contract_id,
                ship.symbol,
                trade_good_symbol,
                ship.cargo.get(trade_good=trade_good).units
            )
            messages.success(request, f'{contract}')
            return redirect('fleet:inventory', pk=ship.symbol)
        
        if request.POST.get('jettison_cargo'):
            ship = Ship.objects.get(symbol=request.POST.get("ship_symbol"))
            trade_good_symbol = request.POST.get("trade_good")
            trade_good = TradeGood.objects.get(symbol=trade_good_symbol)
            print(f'Jettisoning {trade_good} from {ship} at {ship.nav.waypoint}...')
            api = SpaceTradersAPI(request.user.token)
            cargo = api.ship_jettison_cargo(
                ship.symbol,
                trade_good_symbol,
                ship.cargo.get(trade_good=trade_good).units
            )
            return redirect('fleet:inventory', pk=ship.symbol)