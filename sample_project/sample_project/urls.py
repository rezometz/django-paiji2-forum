from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^', include('home.urls')),
    url(r'^', include('forum.urls', namespace='forum')),
    url(r'^admin/', include(admin.site.urls)),
]
