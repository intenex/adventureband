from django.conf.urls.defaults import patterns, include, url
from band.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('band.views',
    (r'^$', index),
    (r'^register/$', register),
    (r'^login/$', login_view),
    (r'^logout/$', logout_view),
    (r'^login/check/$', check_login),
    (r'^create/$', create_character),
    (r'^start/$', choose_character),
    (r'^first/$', first),
    (r'^venture/$', venture),
    (r'^town/$', town),
    (r'^dungeon/$', dungeon),
    (r'^delete/$', delete_char),
    (r'^deselect/$', deselect),
    (r'^town/general/$', town_general),
    (r'^town/weapons/$', town_weapons),
    (r'^town/armory/$', town_armory),
    (r'^town/magic/$', town_magic),
    (r'^town/temple/$', town_temple),
    (r'^town/alchemist/$', town_alchemist),
    (r'^town/market/$', town_market),
    (r'^town/home/$', town_home),
    # Examples:
    # url(r'^$', 'mmo.views.home', name='home'),
    # url(r'^mmo/', include('mmo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)