from django.urls import re_path, path
from django.views.generic.detail import DetailView

from .models import Event
from .views import (EventDetail,
                    EventList,
                    EventCreate,
                    EventUpdate,
                    EventDelete,
                    EventsFeed,
                    EventParticipationList,
                    EventParticipationCreate,
                    EventParticipationDetail,
                    EventParticipationDelete,
                    EventParticipationDownload,
                    ReportEventView)

urlpatterns = [
    path('', EventList.as_view(), name='events_list_all'),
    path('rss', EventsFeed(), name='events_feed'),
    path('<int:pk>/', EventDetail.as_view(), name='detail'),
    path('add/', EventCreate.as_view(), name='add'),
    path('<int:pk>/editar/', EventUpdate.as_view(), name='edit'),
    path('<int:pk>/borrar/', EventDelete.as_view(), name='delete'),
    re_path(r'^(?P<slug>[\w-]+)/$', DetailView.as_view(model=Event), name='event_slug'),

    # Event Registration Management
    path('<int:pk>/inscribirse/', EventParticipationCreate.as_view(), name='register'),
    path('<int:pk>/inscriptos/', EventParticipationList.as_view(), name='registered'),
    path('<int:pk>/inscriptos/csv/', EventParticipationDownload.as_view(), name='registered_csv'),
    path(
        '<int:pk>/inscripcion/<int:participation_pk>/',
        EventParticipationDetail.as_view(),
        name='registration'
    ),
    path(
        '<int:pk>/inscripcion/<int:participation_pk>/borrar/',
        EventParticipationDelete.as_view(),
        name='unregister'
    ),
    path('<int:event_id>/reportar/', ReportEventView.as_view(), name='report'),
]
