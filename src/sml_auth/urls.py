from django.conf.urls import url
from django.contrib import admin

from sml_auth import views


urlpatterns = [
    url(r'^$', views.RegistrationView.as_view(), name='registration'),
    url(r'login/$', views.LoginView.as_view(), name='login')
]
