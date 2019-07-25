from django.conf.urls import url
from django.contrib import admin

from test_assignment import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^authorize-token/$', views.authorize, name='authorize'),
    url(r'^admin/', admin.site.urls),
]
