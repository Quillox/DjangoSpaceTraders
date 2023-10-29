from django.shortcuts import render
from django.views import generic

from .models import Fleet


class IndexView(generic.ListView):
    template_name = 'fleet/index.html'
    context_object_name = 'fleet_list'

    def get_queryset(self):
        return Fleet.objects.all()


class DetailView(generic.DetailView):
    model = Fleet
    template_name = 'fleet/detail.html'

