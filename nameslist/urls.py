from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

import nameslist_app.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nameslist.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin', include(admin.site.urls)),

    url(r'^login', 'django.contrib.auth.views.login', {
        'template_name': 'login.html'
    }),
    url(r'^logout', 'django.contrib.auth.views.logout', {
        'next_page': '/'
    }),
    url(r'', include(nameslist_app.urls)),
)

if settings.DEBUG:
    debugpatterns = patterns('',
                             url(r'list', 'nameslist_app.views.list_debug'))
    urlpatterns += patterns('',
                            url(r'debug', include(debugpatterns)))