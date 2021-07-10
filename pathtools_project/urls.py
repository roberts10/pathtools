"""pathtools_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from dx_search import views
from django.conf.urls import include
from django.views.generic import RedirectView

urlpatterns = [
    #url(r'^pathtools/', include('dx_search.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^dx_search/', include('dx_search.urls')),
    #url(r'^accounts/', include('registration.backends.simple.urls')),
    #url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/', include('registration.backends.admin_approval.urls')),
    url(r'^$', RedirectView.as_view(url = '/dx_search/')),
]

