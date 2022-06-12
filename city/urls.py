from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name="index"),
    path('<int:year>/<str:month>/',views.calendars,name="calendars"),
    path('events',views.events,name="events"),
    path('venues',views.venues,name="venues"),
    path('venues/<int:venue_id>',views.show_venues,name="show_venues"),
    path('events/<int:event_id>',views.clickEvent,name="clickEvent"),
    # CRUD
    path('addvenue',views.addvenue,name="addvenue"),
    path('update_venue/<venue_id>',views.update_venue,name="update_venue"),
    path('update_event/<event_id>',views.update_event,name="update_event"),
    path('delete_event/<event_id>',views.delete_event,name="delete_event"),
    path('addevent',views.addevent,name="addevent"),
    path('delete_venue/<venue_id>',views.delete_venue,name="delete_venue"),
    path('search',views.searchs,name="searchs"),

    path('venue_text',views.venue_text,name="venue_text"),
    path('venue_pdf',views.venue_pdf,name="venue_pdf"),
    path('venue_csv',views.venue_csv,name="venue_csv")
]   