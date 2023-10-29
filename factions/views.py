from django.shortcuts import render
from django.views import generic

from .models import Faction


class IndexView(generic.ListView):
    template_name = 'factions/index.html'
    context_object_name = 'faction_list'

    def get_queryset(self):
        return Faction.objects.all()


class DetailView(generic.DetailView):
    model = Faction
    template_name = 'factions/detail.html'
