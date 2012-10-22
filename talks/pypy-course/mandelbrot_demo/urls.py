from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^render$', 'pypy_demo.mandelbrot.views.render'),
    (r'^pypy_render$', 'pypy_demo.mandelbrot.views.pypy_render'),
    (r'^empty$', 'pypy_demo.mandelbrot.views.empty'),       

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
