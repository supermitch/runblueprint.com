from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='plans/home.html'), name='home'),

    url(r'^plans/$', views.index, name='plans'),
    url(r'^download/$', views.download, name='download'),

    url(r'^about/$', TemplateView.as_view(template_name='plans/about.html'), name='about'),
    url(r'^contact/$', TemplateView.as_view(template_name='plans/contact.html'), name='contact'),
]
