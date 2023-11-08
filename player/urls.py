from django.urls import path

from . import views

app_name = 'player'

urlpatterns = [
    path('home', views.HomeView.as_view(), name='home'),
    path('markets', views.MarketIndexView.as_view(), name='market_index'),
]
