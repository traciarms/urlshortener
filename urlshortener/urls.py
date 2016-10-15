"""urlshortener URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from shortenersite.views import index, redirect_original, shorten_url, \
    create_user, urlset

urlpatterns = [
    url(r'^logout/', auth_views.logout, {'next_page': "/"},
        name='logout'),
    url(r'^login/', auth_views.login,
        {'extra_context': {'next': '/'}}, name='login'),

    url(r'^$', index, name='home'),
    url(r'^register/', create_user, name='register'),
    url(r'^admin/', admin.site.urls),

    url(r'^set/', urlset, name='urlset'),
    url(r'^(?P<short_id>\w{6})$', redirect_original, name='redirectoriginal'),
    url(r'makeshort', shorten_url, name='shortenurl'),
]
