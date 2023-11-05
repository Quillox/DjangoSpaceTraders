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


class WaypointDetailView(generic.DetailView):
    model = Waypoint
    template_name = 'systems/waypoint_detail.html'

    def post(self, request, *args, **kwargs):
        if request.POST.get('update_market'):
            print(f'Updating market {request.POST.get("waypoint_id")}...')
            market = SpaceTradersAPI.get_add_market(request.POST.get('market_symbol'))
            messages.success(request, f'Market {market} successfully updated!')
            return redirect('systems:waypoint_detail', pk=market.pk)
        return super().get(request, *args, **kwargs)