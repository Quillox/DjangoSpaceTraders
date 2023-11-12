from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from .models import Ship, ShipNav, ShipCargoInventory
from player.api import SpaceTradersAPI


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
        
        
class InventoryView(generic.ListView):
    template_name = 'fleet/inventory.html'
    context_object_name = 'inventory_list'

    def get_queryset(self):
        return ShipCargoInventory.objects.filter(ship=self.kwargs['pk']).all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ship'] = Ship.objects.get(symbol=self.kwargs['pk'])
        return context
    
    def post(self, request, *args, **kwargs):
        ship = Ship.objects.get(symbol=self.kwargs['pk'])
        if request.POST.get('update_inventory'):
            print(f'Updating inventory for {ship}...')
            api = SpaceTradersAPI(request.user.token)
            inventory = api.get_ship_cargo(ship.symbol)
            messages.success(request, f'Updated inventory for {ship}!')
            return redirect('fleet:inventory', pk=ship.symbol)


