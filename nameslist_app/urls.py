__author__ = 'peter@chinetti.me'

from django.conf.urls import patterns, include, url

from nameslist_app import views
photoUrlPatterns = patterns('',
                            # /profile/<pid>/photo{'','/'} gives the best photo
                            url(r'(^$|^/$)', views.photo),
                            # /profile/<pid>/photo/<photo_id> gives the specific photo
                            url(r'^/(?P<photo_id>\d)', views.photo),
                            # /profile/<pid>/photo/{'list','add','delete'} do those actions
                            url(r'^/(?P<action>(add|delete|list))($|/$)', views.photo),
                            )
nameUrlPatterns = patterns('',
                           # /profile/<pid>/name{'','/'} gives the correct name
                           url(r'(^$|^/$)', views.name),
                           # You can only add a name, who cares about listing all the
                           # wrong ones or deleting
                           url(r'^/add($|/$)', views.name, {'action': 'add'}),
                           )
factUrlPatterns = patterns('',
                           # /profile/<pid>/fact exists, lists all the facts
                           # about that guy
                           url(r'^$|^/$', views.fact),
                           # /profile/<pid>/fact/add adds
                           url(r'^/add$|^/$', views.fact, {'action': 'add'}),
                           # /profile/<pid>/fact/<fact_id> fetches that answer id
                           url(r'^/(?P<fact_id>)$|^/$', views.fact),
                           )
opinionUrlPatterns = patterns('',
                              # /profile/<pid>/opinion exists, lists all the opinions
                              # about that guy
                              url(r'^$|^/$', views.opinion),
                              # /profile/<pid>/opinion/add adds
                              url(r'^/add$|^/$', views.opinion, {'action': 'add'}),
                              # /profile/<pid>/opinion/<opinion_id> fetches that answer id
                              url(r'^/(?P<opinion_id>)$|^/$', views.opinion),
                              )
profileActionPatterns = patterns('',
                                 url(r'^$|^/$', views.profile),
                                 url(r'^photo', include(photoUrlPatterns)),
                                 url(r'^name', include(nameUrlPatterns)),
                                 url(r'^fact', include(factUrlPatterns)),
                                 url(r'^opinion', include(opinionUrlPatterns)),
                                 )

profileUrlPatterns = patterns('',
                              url(r'^(?P<prospective_id>\d)'), include(profileActionPatterns)
                              )

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^submit/', views.submit, name='submit'),
                       url(r'^profile/', include(profileUrlPatterns)),
                       )

