from django.conf.urls import url, include
from django.conf import settings
from importlib import import_module

from django.core.handlers.wsgi import get_script_name
from django.urls import set_script_prefix
set_script_prefix(get_script_name({}))

api_module = import_module('.'.join(settings.TASTYPIE_DOC_API.split('.')[:-1]))
try:
    version = api_module.__version__
except AttributeError:
    version = None

info = getattr(settings, 'API_INFO')

urlpatterns =[
    url(r'^chembl_webservices/', include('chembl_webservices.urls')),
    url(r'^chembl_webservices/', include('tastypie_spore_docs.urls'))
]


def handler500(request):
    """
    500 error handler which includes ``request`` in the context.
    Templates: `500.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('500.html') # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'request': request,
})))
