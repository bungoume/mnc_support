from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mnc_support.views.home', name='home'),
    # url(r'^mnc_support/', include('mnc_support.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^daybook/$', 'daybook.views.index'),
    (r'^daybook/classList$', 'daybook.views.classList'),
    (r'^daybook/lesson$', 'daybook.views.showLesson'),
    (r'^daybook/lesson/(?P<id>\d+)/$', 'daybook.views.showLesson'),
    (r'^daybook/classList/update$', 'daybook.views.updateClassList'),
)
