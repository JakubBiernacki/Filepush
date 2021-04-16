from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView

from api.models import Sharedir


class HomeView(LoginView):
    template_name = 'view/home.html'
    # redirect_authenticated_user = True


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


class ShareDirView(DetailView):
    model = Sharedir
    template_name = 'view/sharedir.html'
    slug_field = 'code'
    slug_url_kwarg = 'code'

    def get_object(self, queryset=None):
        code = self.kwargs['code']
        self.dir = get_object_or_404(Sharedir.objects.prefetch_related('file_set').select_related(
            'user'), code=code)
        return self.dir
