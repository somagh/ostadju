from django.conf.urls import url
from django.contrib.auth import views as auth_views

from people.views import signup, contact_us, profile, edit_profile, SearchProfiles, new_teacher_free_time, \
    teacher_free_times, delete_teacher_free_time, search_teachers_api_view

urlpatterns = [
    url(r'^signup/$', signup, name="signup"),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='people/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^contact_us/$', contact_us, name="contact_us"),
    url(r'^profile/(?P<username>.*)/$', profile, name="profile"),
    url(r'^edit_profile/$', edit_profile, name="edit_profile"),
    url(r'^search_profiles/', SearchProfiles.as_view(), name="search_profiles"),
    url(r'^new_free_time$', new_teacher_free_time, name="new_free_time"),
    url(r'^delete_free_time/(?P<free_time_id>\d+)/$', delete_teacher_free_time, name="delete_free_time"),
    url(r'^teacher_free_times/(?P<teacher_username>.*)/$', teacher_free_times, name="teacher_free_times"),
    url(r'^search_teachers_api/$', search_teachers_api_view, name="search_teachers_api")
]
