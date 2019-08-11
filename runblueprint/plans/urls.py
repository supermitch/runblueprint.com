from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='plans/home.html'), name='home'),

    url(r'^plans/$', views.index, name='plans'),
    url(r'^download/$', views.download, name='download'),

    url(r'^about/$', TemplateView.as_view(template_name='plans/about.html'), name='about'),
    url(r'^contact/$', TemplateView.as_view(template_name='plans/contact.html'), name='contact'),
    url(r'^account/$', views.account, name='account'),
    url(r'^login/$', auth_views.LoginView.as_view(), name="login"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # TODO: Development only?
