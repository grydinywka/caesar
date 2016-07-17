"""caesar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import patterns, include, url
from django.contrib import admin
from caesarapp import views
from django.views.i18n import javascript_catalog

js_info_dict = {
    'packages': ('caesarapp',),
}

urlpatterns = [
    # index page
    url(r'^$', views.index, name='index'),
    url(r'^second/$', views.second, name='second'),
    url(r'^diagr/$', views.diagr, name='diagr'),
    url(r'^jsi18n\.js$', javascript_catalog, js_info_dict, name='jsi18n'),

    # admin page
    url(r'^admin/', include(admin.site.urls)),
]
