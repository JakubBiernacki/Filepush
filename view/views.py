from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, RedirectView
from django.db.models import Sum, Count
from api.models import Sharedir


class HomeView(LoginView):
    template_name = 'view/home.html'
    # redirect_authenticated_user = True


# class DashboardView(LoginRequiredMixin, ListView):
#     model = Sharedir
#     template_name = 'view/dashboard.html'
#
#     def get_queryset(self):
#         user = self.request.user
#         queryset = Sharedir.objects.all().select_related(
#             'user').filter(user=user).order_by("-created_at")
#
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super(DashboardView, self).get_context_data(**kwargs)
#         context['size'] = sum([x.size for x in self.get_queryset()])
#         return context

def dashboard(request):
    user = request.user

    queryset = Sharedir.objects.defer('user').annotate(file_count=Count('file')).filter(user=user).order_by("-created_at")

    size = sum([x.size for x in queryset])

    context = {
        'object_list': queryset,
        'size': size
    }

    return render(request, 'view/dashboard.html', context)


class AdddirView(LoginRequiredMixin, TemplateView):
    template_name = 'view/adddir.html'


class ShareDirView(DetailView):
    model = Sharedir
    template_name = 'view/sharedir.html'
    slug_field = 'code'
    slug_url_kwarg = 'code'

    def get_object(self, queryset=None):
        code = self.kwargs['code']
        sharedir = get_object_or_404(Sharedir.objects.prefetch_related('file_set').select_related(
            'user'), code=code)
        return sharedir
