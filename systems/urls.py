from django.urls import path

from . import views

app_name = 'systems'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<str:pk>/', views.DetailView.as_view(), name='detail'),
    path('<str:system_symbol>/waypoints/', views.WaypointIndexView.as_view(), name='waypoint_index'),
    path('<str:system_symbol>/waypoints/<str:pk>/', views.WaypointDetailView.as_view(), name='waypoint_detail'),
    path('<str:system_symbol>/waypoints/<str:pk>/market/', views.MarketDetailView.as_view(), name='market_detail'),
    path('<str:system_symbol>/waypoints/<str:pk>/shipyard/', views.ShipyardDetailView.as_view(), name='shipyard_detail'),
    path('<str:system_symbol>/waypoints/<str:pk>/shipyard/ships/<int:ship_id>/', views.ShipyardShipDetailView.as_view(), name='shipyard_ship_detail'),
]
