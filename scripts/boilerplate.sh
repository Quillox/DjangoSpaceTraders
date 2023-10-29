#!/bin/bash

# Create urls.py files
echo "Creating urls.py files..."
cat << EOF > contracts/urls.py
from django.urls import path

from . import views

app_name = 'contracts'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<str:pk>/', views.DetailView.as_view(), name='detail'),
]
EOF

cat << EOF > fleet/urls.py
from django.urls import path

from . import views

app_name = 'fleet'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<str:pk>/', views.DetailView.as_view(), name='detail'),
]
EOF

cat << EOF > systems/urls.py
from django.urls import path

from . import views

app_name = 'systems'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<str:pk>/', views.DetailView.as_view(), name='detail'),
]
EOF

# Create views.py files
echo "Creating views.py files..."
cat << EOF > contracts/views.py
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
EOF

cat << EOF > fleet/views.py
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
EOF

cat << EOF > systems/views.py
from django.shortcuts import render
from django.views import generic

from .models import System


class IndexView(generic.ListView):
    template_name = 'systems/index.html'
    context_object_name = 'system_list'

    def get_queryset(self):
        return System.objects.all()


class DetailView(generic.DetailView):
    model = System
    template_name = 'systems/detail.html'
EOF

# Create index.html files
echo "Creating index.html files..."
cat << EOF > contracts/templates/contracts/index.html
{% extends 'base_contracts.html' %}

{% block content %}
<h1>Contracts</h1>
{% if contract_list %}
<ul>
{% for contract in contract_list %}
<li><a href="{% url 'contracts:detail' contract.pk %}">{{ contract.name }}</a></li>
{% endfor %}
</ul>
{% else %}
<p>No contracts are available.</p>
{% endif %}
{% endblock %}
EOF

cat << EOF > fleet/templates/fleet/index.html
{% extends 'base_fleet.html' %}

{% block content %}
<h1>Fleet</h1>
{% if fleet_list %}
<ul>
{% for fleet in fleet_list %}
<li><a href="{% url 'fleet:detail' fleet.pk %}">{{ fleet.name }}</a></li>
{% endfor %}
</ul>
{% else %}
<p>No fleets are available.</p>
{% endif %}
{% endblock %}
EOF

cat << EOF > systems/templates/systems/index.html
{% extends 'base_systems.html' %}

{% block content %}
<h1>Systems</h1>
{% if system_list %}
<ul>
{% for system in system_list %}
<li><a href="{% url 'systems:detail' system.pk %}">{{ system.name }}</a></li>
{% endfor %}
</ul>
{% else %}
<p>No systems are available.</p>
{% endif %}
{% endblock %}
EOF

# Create detail.html files
echo "Creating detail.html files..."
cat << EOF > contracts/templates/contracts/detail.html
{% extends 'base_contracts.html' %}

{% block content %}
<h1>Contract details</h1>
{{ contract }}
{% endblock %}
EOF

cat << EOF > fleet/templates/fleet/detail.html
{% extends 'base_fleet.html' %}

{% block content %}
<h1>Fleet details</h1>
{{ fleet }}
{% endblock %}
EOF

cat << EOF > systems/templates/systems/detail.html
{% extends 'base_systems.html' %}

{% block content %}
<h1>System details</h1>
{{ system }}
{% endblock %}
EOF

echo "Done!"