from django.urls import path

from api import views

urlpatterns = [
    path('contribs/', views.GithubContribs.as_view(), name='api-contribs'),
    path('repos/', views.GithubRepos.as_view(), name='api-repos'),
    path('langs/', views.TopLangs.as_view(), name='api-langs'),
]