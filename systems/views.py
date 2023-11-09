from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect

from .models import System, Waypoint
from player.api import SpaceTradersAPI


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

    def post(self, request, *args, **kwargs):
        if request.POST.get('update_market'):
            print(f'Updating market {request.POST.get("waypoint_id")}...')
            market = SpaceTradersAPI.get_add_market(request.POST.get('market_symbol'))
            messages.success(request, f'Market {market} successfully updated!')
            return redirect('systems:waypoint_detail', pk=market.pk)
        elif request.POST.get('update_waypoint'):
            print(f'Updating waypoint {request.POST.get("waypoint_id")}...')
            waypoint = SpaceTradersAPI.add_waypoint(request.POST.get('waypoint_id'))
            messages.success(request, f'Waypoint {waypoint} successfully updated!')
            return redirect('systems:waypoint_detail', pk=waypoint.pk)
        return super().get(request, *args, **kwargs)
