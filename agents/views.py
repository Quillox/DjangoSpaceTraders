from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Agent
from .forms import TokenForm
from player.api import SpaceTradersAPI

class EnterTokenView(LoginRequiredMixin, FormView):
    template_name = 'agents/enter_token.html'
    form_class = TokenForm

    def get_success_url(self):
        return reverse('player:home')

    def form_valid(self, form):
        self.request.user.token = form.cleaned_data['token']
        self.request.user.save()
        messages.success(self.request, 'SpaceTraders API token saved successfully!')

        # Add the users agent to the database
        messages.info(self.request, 'Adding your agent to the database...')
        api = SpaceTradersAPI(self.request.user.token)
        agent = api.get_add_my_agent()
        self.request.user.agent = agent
        self.request.user.save()
        messages.success(self.request, f'Agent {agent.symbol} successfully added to the database and linked with account {self.request.user.username}!')
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.token is not None and SpaceTradersAPI.validate_token(request.user.token):
            # Update the users agent in the database
            messages.info(request, 'Updating your agent in the database...')
            api = SpaceTradersAPI(request.user.token)
            agent = api.get_add_my_agent()
            request.user.agent = agent
            request.user.save()
            messages.success(request, f'Agent {agent.symbol} successfully added to the database!')
            return redirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

class IndexView(generic.ListView):
    template_name = 'agents/index.html'
    context_object_name = 'agent_list'

    def get_queryset(self):
        return Agent.objects.all()

class DetailView(generic.DetailView):
    model = Agent
    # THis is the default template name
    template_name = 'agents/detail.html'

    def post(self, request, *args, **kwargs):
        if request.POST.get('update'):
            if request.user.agent.symbol == self.get_object().symbol:
                messages.info(request, 'Updating your agent in the database...')
                api = SpaceTradersAPI(request.user.token)
                agent = api.get_add_my_agent()
                request.user.agent = agent
                request.user.save()
                messages.success(request, f'Agent {agent.symbol} successfully updated in the database!')
                return redirect('agents:detail', pk=agent.symbol)
            else:
                messages.info(request, f'Updating agent {self.get_object().symbol} in the database...')
                SpaceTradersAPI.get_add_public_agent(self.get_object().symbol)
                messages.success(request, f'Agent {self.get_object().symbol} successfully updated in the database!')
                return redirect('agents:detail', pk=self.get_object().symbol)
        return super().get(request, *args, **kwargs)

