from django.conf.urls import url, include
from django.contrib import admin

from sml import  views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^registration/', include('sml_auth.urls', namespace='sml_auth')),
    url(r'^api/', include('sml_auction.urls', namespace='api')),
]
