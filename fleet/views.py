from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from .models import Ship, ShipNav
from player.api import SpaceTradersAPI


class IndexView(generic.ListView):
    template_name = 'fleet/index.html'
    context_object_name = 'fleet_list'

    def get_queryset(self):
        return Ship.objects.filter(agent=self.request.user.agent.pk).all()

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
        
        

