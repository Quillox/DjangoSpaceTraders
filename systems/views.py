from django import forms
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from .models import System, Waypoint, Market, JumpGate
from player.api import SpaceTradersAPI
from fleet.models import Shipyard, ShipyardShip, Ship


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


class UpdateWaypointForm(forms.Form):
    update_waypoint = forms.BooleanField()

class NavigateShipForm(forms.ModelForm):
    class Meta:
        model = Ship
        fields = ['symbol']


def update_waypoint(request, waypoint_symbol):
    if request.method == 'POST':
        pass


class WaypointDetailView(generic.DetailView):
    model = Waypoint
    template_name = 'systems/waypoint_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fleet'] = Ship.objects.filter(agent=self.request.user.agent.pk).all()
        return context

    def post(self, request, *args, **kwargs):
        waypoint_symbol = self.get_object().symbol
        update_form = UpdateWaypointForm(request.POST, prefix='update')
        navigate_form = NavigateShipForm(request.POST, prefix='navigate')

        if update_form.is_valid():
            print(f'Updating waypoint {waypoint_symbol}...')
            waypoint = SpaceTradersAPI.update_waypoint(waypoint_symbol)
            messages.success(request, f'Waypoint {waypoint} successfully updated!')
            return redirect('systems:waypoint_detail', system_symbol=waypoint.system.symbol, pk=waypoint.pk)

        elif navigate_form.is_valid():
            print('jam')
            print(f'Navigating ship {navigate_form.cleaned_data["ship_id"]} to waypoint {waypoint_symbol}...')

        return super().get(request, *args, **kwargs)

class MarketDetailView(generic.DetailView):
    model = Market
    template_name = 'systems/market_detail.html'

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