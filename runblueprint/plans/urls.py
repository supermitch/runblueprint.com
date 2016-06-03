from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='plans'),
    url(r'^download/$', views.download, name='download'),
]
