from django.shortcuts import render
from django.views import generic

from .models import Contract


class IndexView(generic.ListView):
    template_name = 'contracts/index.html'
    context_object_name = 'contract_list'

    def get_queryset(self):
        return Contract.objects.all()


class DetailView(generic.DetailView):
    model = Contract
    template_name = 'contracts/detail.html'

