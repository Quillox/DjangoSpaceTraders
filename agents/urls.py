from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

app_name = 'agents'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('enter_token/', views.enter_token, name='enter_token'),
    path("<str:pk>/", views.DetailView.as_view(), name="detail"),
    path('register_agent/', views.register_agent, name='register_agent'),
]