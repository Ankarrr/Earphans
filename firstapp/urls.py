from django.conf.urls import url

from . import views

# namespace for urls
app_name = 'firstapp'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # ex: /firstapp/5
    # r = raw, It tells Python that a string is “raw” – that nothing in the string should be escaped.
    # (?P<name>pattern), where name is the name of the group and pattern is some pattern to match.
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /firstapp/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /firstapp/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
