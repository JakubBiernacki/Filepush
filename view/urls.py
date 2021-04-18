from django.urls import path, include, re_path
from .views import *
from allauth.account.urls import urlpatterns
from allauth.account.views import signup, confirm_email, email_verification_sent
from django.views.generic import RedirectView


urlpatterns = [
    path('', HomeView.as_view(), name='account_login'),  # login
    path('', HomeView.as_view(), name='home'),  # login
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/adddir/', AdddirView.as_view(), name='adddir'),

    path('sharedir/<str:code>/', ShareDirView.as_view(), name='dir'),

    # path('', include('allauth.urls')),

]

# allauth

urlpatterns += [
    path('register/', signup, name='account_signup'),

    path('inactive/', RedirectView.as_view(pattern_name='home'), name='account_inactive'),

    path(
        "confirm-email/",
        email_verification_sent,
        name="account_email_verification_sent",
    ),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        confirm_email,
        name="account_confirm_email",
    )

]
