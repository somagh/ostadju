from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from people import views


urlpatterns = [
    url(r'^signup/$', views.signup, name="signup"),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='people/login.html'), name='login'),
]
