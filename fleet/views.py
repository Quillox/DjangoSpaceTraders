from django.shortcuts import render
from django.views import generic

from .models import Ship, ShipNav


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

