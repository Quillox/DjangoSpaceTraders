from django.urls import path

from . import views

app_name = 'systems'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<str:pk>/', views.DetailView.as_view(), name='detail'),
    path('<str:system_symbol>/waypoints/<str:pk>/', views.WaypointDetailView.as_view(), name='waypoint_detail'),
]
