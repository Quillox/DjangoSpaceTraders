from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

app_name = 'agents'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('enter-token/', views.EnterTokenView.as_view(), name='enter-token'),
    path("<str:pk>/", views.DetailView.as_view(), name="detail"),
]