"""
URL configuration for spaceTraders project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

`path('accounts/', include('django.contrib.auth.urls')),` gives:
- accounts/login/ [name='login']
- accounts/logout/ [name='logout']
- accounts/password_change/ [name='password_change']
- accounts/password_change/done/ [name='password_change_done']
- accounts/password_reset/ [name='password_reset']
- accounts/password_reset/done/ [name='password_reset_done']
- accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
- accounts/reset/done/ [name='password_reset_complete']
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('agents/', include('agents.urls')),
    path('contracts/', include('contracts.urls')),
    path('factions/', include('factions.urls')),
    path('fleet/', include('fleet.urls')),
    path('player/', include('player.urls')),
    path('systems/', include('systems.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]