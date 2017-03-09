from django.conf.urls import url

from . import views

# namespace for urls
app_name = 'firstapp'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    # ex: /firstapp/5
    # r, raw, It tells Python that a string is “raw” – that nothing in the string should be escaped.
    # ^, start
    # (?P<name>pattern), where name is the name of the group and pattern is some pattern to match.
    # pk, The DetailView generic view expects the primary key value captured from the URL to be called "pk", so we’ve changed question_id to pk for the generic views.
    # $, finish
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # ex: /firstapp/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),

    # ex: /firstapp/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
