from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url
from tutoring import views

urlpatterns = patterns('',
    url(r'^mentor/add/$', login_required(views.AddMentor.as_view()), name='new_mentor'),
    url(r'^mentor/update/(?P<pk>[0-9]+)/$', login_required(views.UpdateMentor.as_view()), name='update_mentor'),
    url(r'^mentor/delete/(?P<pk>[0-9]+)/$', login_required(views.DeleteMentor.as_view()), name='delete_mentor'),
    url(r'^mentor/(?P<pk>[0-9]+)/$', views.DisplayMentor.as_view(), name='display_mentor'),
    url(r'^apprentice/add/$', views.AddApprentice.as_view(), name='new_apprentice'),
    url(r'^project/add/$', views.AddProject.as_view(), name='new_project'),
    # url(r'^(?P<tutoring_id>\d+)/$', views.detail, name='detail'),
)