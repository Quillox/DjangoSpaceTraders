from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views import generic

from .models import Agent
from player.api import SpaceTradersAPI


@login_required
def enter_token(request):
    # Check to see if the user has a valid token
    if request.user.token is not None and SpaceTradersAPI.validate_token(request.user.token):
        # Update the users agent in the database
        messages.info(request, 'Updating your agent in the database...')
        api = SpaceTradersAPI(request.user.token)
        agent = api.get_add_my_agent()
        request.user.agent = agent
        request.user.save()
        messages.success(request, f'Agent {agent.symbol} successfully added to the database!')
        return redirect('player:home')
    else:
        if request.method == 'POST':
            token = request.POST.get('token')
            if SpaceTradersAPI.validate_token(token):
                request.user.token = token
                request.user.save()
                messages.success(request, 'SpaceTraders API token saved successfully!')

                # Add the users agent to the database
                messages.info(request, 'Adding your agent to the database...')
                api = SpaceTradersAPI(request.user.token)
                agent = api.get_add_my_agent()
                request.user.agent = agent
                request.user.save()
                messages.success(request, f'Agent {agent.symbol} successfully added to the database and linked with account {request.user.username}!')
                return redirect('player:home')
            else:
                messages.error(request, 'Please enter a valid token.')
        return render(request, 'agents/enter_token.html')

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


# @login_required
# def register_agent(request):
#     if request.method == 'POST':
#         if 'register_agent' in request.POST:
#             # Get the required information from the user
#             agent_symbol = request.POST.get('agent_symbol')
#             starting_faction = request.POST.get('starting_faction')

#             messages.success(
#                 request, f'Agent {agent_symbol} successfully registered with the {starting_faction} faction!')
#             return redirect('home')
#         elif 'add_agent' in request.POST:
#             api = SpaceTradersAPI(request.user.token)
#             agent_details = api.get_token('my/agent')['data']
#             agent = Agent.add(agent_details)
#             agent.save()
#             messages.success(
#                 request, f'Agent {agent.symbol} successfully added to the database!')

#     return render(request, 'agents/register_agent.html')


