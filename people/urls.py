from django.conf.urls import url
from django.contrib.auth import views as auth_views

from people.views import signup, contact_us, profile, edit_profile, SearchProfiles, new_teacher_free_time

urlpatterns = [
    url(r'^signup/$', signup, name="signup"),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='people/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^contact_us/$', contact_us, name="contact_us"),
    url(r'^profile/(?P<username>.*)/$', profile, name="profile"),
    url(r'^edit_profile/$', edit_profile, name="edit_profile"),
    url(r'^search_profiles/', SearchProfiles.as_view(), name="search_profiles"),
    url(r'^new_free_time$', new_teacher_free_time, name="new_free_time"),
]
