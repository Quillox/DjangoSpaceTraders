from django.urls import path

from . import views

app_name = 'player'

urlpatterns = [
    path('home', views.HomeView.as_view(), name='home'),
    path('markets', views.MarketIndexView.as_view(), name='market_index'),
    path('construction_sites', views.ConstructionSiteIndexView.as_view(), name='construction_site_index'),
    path('jump_gates', views.JumpGateIndexView.as_view(), name='jump_gate_index'),
    path('shipyards', views.ShipyardIndexView.as_view(), name='shipyard_index'),
]
