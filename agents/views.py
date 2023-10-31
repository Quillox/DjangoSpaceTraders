from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views import generic

from .models import Agent, User
from .api import SpaceTradersAPI


def home(request):
    if request.method == 'POST':
        if request.POST.get('public_agent_symbol'):
            print(f'Adding agent {request.POST.get("public_agent_symbol")} to the database...')
            agent = SpaceTradersAPI.get_add_public_agent(
                request.POST.get('public_agent_symbol')
            )
            messages.success(request, f'Agent {agent.symbol} successfully added to the database!')
            return redirect('agents:detail', pk=agent.symbol)
        elif request.POST.get('contract_id'):
            contract_id = request.POST.get("contract_id")
            print(f'Adding contract {contract_id} to the database...')
            api = SpaceTradersAPI(request.user.token)
            contract = api.get_add_contract(contract_id)
            messages.success(request, f'Contract {contract.id} successfully added to the database!')
            return redirect('contracts:detail', pk=contract.id)
    return render(request, 'agents/home.html')

@login_required
def enter_token(request):
    # Check to see if the user has a valid token
    if request.user.token is not None and SpaceTradersAPI.validate_token(request.user.token):
        # Update the users agent in the database
        messages.info(request, 'Adding your agent in the database...')
        api = SpaceTradersAPI(request.user.token)
        agent = api.get_add_my_agent()
        messages.success(request, f'Agent {agent.symbol} successfully added to the database!')
        return redirect('home')
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
                agent_data = api.get_token('my/agent')['data']
                agent = Agent.add(agent_data)
                request.user.agent = agent
                request.user.save()
                messages.success(request, f'Agent {agent.symbol} successfully added to the database and linked with account {request.user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Please enter a valid token.')
        return render(request, 'agents/enter_token.html')


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


class IndexView(generic.ListView):
    template_name = 'agents/index.html'
    context_object_name = 'agent_list'

    def get_queryset(self):
        return Agent.objects.all()
    


class DetailView(generic.DetailView):
    model = Agent
    # THis is the default template name
    template_name = 'agents/detail.html'

