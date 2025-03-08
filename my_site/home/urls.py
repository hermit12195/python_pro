from django.urls import path, re_path
from . import views

urlpatterns = [
    path('home/', views.home),
    path('about/', views.about, name="Про нас"),
    path('contact/', views.contact, name="Контакти"),
    re_path('^post/(?P<id>\d+)/$', views.post_view),
    re_path(r'^profile/(?P<username>\w+)/$', views.profile_view),
    re_path(r'^event/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.event_view)
]
