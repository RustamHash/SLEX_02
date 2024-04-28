from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect

from base_app.models import Filial


def home(request):
    context = {'filial': Filial.objects.filter(as_active=True)}
    return render(request, 'base_app/home.html', context=context)


class Login(LoginView):
    template_name = 'base_app/login.html'

    def get_success_url(self):
        return super(Login, self).get_success_url()


class NotFound(LoginView):
    template_name = 'base_app/not_groups.html'

    def get_success_url(self):
        return super(NotFound, self).get_success_url()


def logout_view(request):
    logout(request)
    return redirect('home')
