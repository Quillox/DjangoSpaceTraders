from django.urls import path

from . import views

app_name = 'fleet'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<str:pk>/', views.DetailView.as_view(), name='detail'),
    path('<str:pk>/nav/', views.NavView.as_view(), name='nav'),
    path('<str:pk>/inventory/', views.InventoryView.as_view(), name='inventory'),
]
