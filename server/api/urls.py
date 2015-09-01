__author__ = 'abdullah'

from api import views
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

    url(r'^contents$', views.Contents.as_view()),
    url(r'^links', views.Links.as_view()),
    url(r'^contents/(?P<content_link>\w+)$', views.Contents.as_view()),
    # url(r'^users$', views.Users.as_view()),
    url(r'^user/', include('membership.urls')),
    url(r'^tracks/requirements$', views.TrackRequirements.as_view()),
    url(r'^tracks$', views.CompositionView.as_view()),
    url(r'^tracks/(?P<user_id>\d+)$', views.CompositionView.as_view()),
    url(r'^tracks/(?P<list_type>\w+)$', views.CompositionView.as_view()),
    url(r'^vote', views.VoteView.as_view()),
    url(r'^contests$', views.ContestView.as_view()),
    url(r'^contests/(?P<contest_year>\d+)$', views.ContestView.as_view()),
    # url(r'^user($', views.SignUp.as_view()),
    # url(r'^manufacturers$', views.Manufacturers.as_view()),
    # url(r'^extras/$', views.Extras.as_view()),
    # url(r'^auth/', views.AuthView.as_view(), name='auth-view'),
    # url(r'^deneme/', views.Deneme.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
