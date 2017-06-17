from django.views.generic import CreateView, View
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login

from sml_auth.forms import RegistrationForm


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('sml_auth:login')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return HttpResponse(status=400)

        user = authenticate(request, username=username, password=password)

        if user is None:
            return HttpResponse('Username or password isn\'t correct', status=400)

        login(request, user)

        # didn't used reverse because I think that more implicit
        return redirect('/')
