from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages

from .models import Faction
from player.api import SpaceTradersAPI


class IndexView(generic.ListView):
    template_name = 'factions/index.html'
    context_object_name = 'faction_list'

    def get_queryset(self):
        return Faction.objects.all()
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('populate'):
            print(f'Populating factions...')
            messages.info(request, f'Populating factions... this will take a few minutes.')
            SpaceTradersAPI.populate_factions()
            messages.success(request, f'Factions successfully populated!')
            return redirect('factions:index')
        return super().get(request, *args, **kwargs)


class DetailView(generic.DetailView):
    model = Faction
    template_name = 'factions/detail.html'
