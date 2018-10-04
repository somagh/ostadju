from django.conf.urls import url
from django.views.generic import TemplateView
from people import views


urlpatterns = [
    url(r'^signup/$', views.signup, name="signup")
]
