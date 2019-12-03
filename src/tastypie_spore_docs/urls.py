__author__ = 'mnowotka'

from importlib import import_module
from django.conf.urls import url
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from tastypie_spore_docs.direct_template_view import DirectTemplateView
from tastypie_spore_docs.views import generate_spore_endpoint
try:
    from django.utils.module_loading import import_string
except ImportError:
    from django.utils.module_loading import import_by_path as import_string

try:
    api = import_string(settings.TASTYPIE_DOC_API)
except AttributeError:
    raise ImproperlyConfigured('TASTYPIE_DOC_API setting is required')


try:
    name = settings.TASTYPIE_DOC_NAME
except AttributeError:
    name = 'Tastypie REST API documentation'

api_name = api.api_name
api_module = import_module('.'.join(settings.TASTYPIE_DOC_API.split('.')[:-1]))
try:
    version = api_module.__version__
except AttributeError:
    version = api_name

urlpatterns = [
    url(r'^%s/docs' % api_name, DirectTemplateView.as_view(template_name="docs.html"), name='ws_docs'),
    url(r'^%s/spore' % api_name, generate_spore_endpoint, {'api': api, 'name': name, 'version':version}, name='ws_spore_endpoint'),
]
