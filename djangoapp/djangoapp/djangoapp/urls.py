"""djangoapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('webapp.urls')),
    url(r'^signin/', include('webapp.urls')),
    url(r'^wizard/', include('webapp.urls')),
    url(r'^upload/', include('webapp.urls')),
    url(r'^whitelist_upload/', include('webapp.urls')),
    url(r'^ajax/validate_ipaddressform/',include('webapp.urls')),
    url(r'^deployment_quessionnaire/',include('webapp.urls')),
    url(r'^login/',include('webapp.urls')),
]
