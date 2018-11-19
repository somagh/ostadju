from django.conf.urls import url
from django.contrib.auth import views as auth_views

from people.views import signup, contact_us, profile, edit_profile, SearchProfiles, new_teacher_free_time, \
    delete_teacher_free_time, search_teachers_api_view, update_teacher_free_time, seen_notification, reserve_free_time, \
    undo_reserve_free_time, remove_user

app_name = "people"

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
    url(r'^search_teachers_api/$', search_teachers_api_view, name="search_teachers_api"),
    url(r'^update_teacher_free_time/(?P<free_time_id>.*)/$', update_teacher_free_time, name="update_teacher_free_time"),
    url(r'^seen_notification/(?P<notification_id>\d+)/$', seen_notification, name="seen_notification"),
    url(r'^reserve_free_time/(?P<free_time_id>\d+)/$', reserve_free_time, name="reserve_free_time"),
    url(r'^undo_reserve_free_time/(?P<free_time_id>\d+)/$', undo_reserve_free_time, name="undo_reserve_free_time"),
    url(r'^remove_user/$', remove_user, name="remove_user")
]
