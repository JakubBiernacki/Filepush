from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect



from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse
from django.views.generic import TemplateView, ListView

from api.models import Sharedir


class HomeView(LoginView):
    template_name = 'view/home.html'
    redirect_authenticated_user = True



class LogoutuserView(LogoutView):
    pass


class DashboardView(LoginRequiredMixin, ListView):
    model = Sharedir
    template_name = 'view/dashboard.html'

    def get_queryset(self):
        user = self.request.user
        queryset = Sharedir.objects.all().prefetch_related('file_set').select_related(
            'user').filter(user=user).order_by("-creared_at")

        return queryset


class AdddirView(LoginRequiredMixin, TemplateView):
    template_name = 'view/adddir.html'
