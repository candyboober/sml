from django.urls import reverse_lazy
from django.shortcuts import redirect


def index(request):
    return redirect(reverse_lazy('api:auction-list'))
