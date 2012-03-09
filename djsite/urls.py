from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.defaults import *
from django.views.generic import list_detail

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('djsite.views',
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('djsite.wizard.views',
    (r'^$', 'welcome'),
    (r'^project-details/',              'project_details'),
    (r'^mountpoint/',                   'mountpoint'),
    (r'^import-gui/',                   'import_gui'),
    (r'^import-cmd/',                   'import_cmd'),
    (r'^import-cmd-get-progress/',      'import_cmd_get_progress'),
    (r'^import-cmd-is-valid/',          'import_cmd_is_valid'),
    (r'^scantailor/',                   'scantailor'),
)
urlpatterns += staticfiles_urlpatterns()