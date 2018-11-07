from django.conf.urls import url
from django.contrib.auth import views as auth_views

from people import views

urlpatterns = [
    url(r'^signup/$', views.signup, name="signup"),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='people/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^contact_us/$', views.contact_us, name="contact_us"),
    url(r'^profile/$', views.profile, name="profile"),
]
