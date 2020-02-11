__author__ = 'mnowotka'

import time
import requests
from tastypie.utils import trailing_slash
from tastypie import http
from tastypie import fields
from tastypie.exceptions import NotFound
from tastypie.exceptions import BadRequest
from django.conf import settings
from django.conf.urls import url
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from chembl_webservices.core.resource import ChemblModelResource
from chembl_webservices.core.resource import WS_DEBUG
from chembl_webservices.core.meta import ChemblResourceMeta
from chembl_webservices.core.serialization import ChEMBLApiSerializer
from chembl_webservices.resources.molecule import MoleculeResource

from chembl_core_model.models import CompoundStructures
from chembl_core_model.models import MoleculeDictionary
from django.views.decorators.csrf import csrf_exempt



from chembl_webservices.core.fields import monkeypatch_tastypie_field
monkeypatch_tastypie_field()

SUPPORTED_ENGINES = ['rdkit']
BEAKER_CTAB_TO_SVG_URL = settings.BEAKER_URL + '/ctab2svg'

fakeSerializer = ChEMBLApiSerializer('image')
fakeSerializer.formats = ['svg']

available_fields = [f.name for f in MoleculeDictionary._meta.fields]

# ----------------------------------------------------------------------------------------------------------------------


class ImageResource(ChemblModelResource):

# ----------------------------------------------------------------------------------------------------------------------

    image = fields.ApiField()

    class Meta(ChemblResourceMeta):
        resource_name = 'image'
        serializer = fakeSerializer
        default_format = 'image/svg+xml'
        fields = ('image',)
        description = {'api_dispatch_detail' : '''
Get image of the compound, specified by

*  _ChEMBL ID_ or
*  _Standard InChI Key_

You can specify optional parameters:

*  __engine__ - chemistry toolkit used for rendering, can be _rdkit_ only, default: _rdkit_.
*  __dimensions__ - size of the image (the length of the square image side). Can't be more than _500_, default: _500_.
*  __ignoreCoords__ - Ignore 2D coordinates encoded in the molfile and let the chemistry toolkit to recompute them.


'''}
        queryset = CompoundStructures.objects.all() if 'downgraded' not in available_fields else \
                        CompoundStructures.objects.exclude(molecule__downgraded=True)


# -----------------------------------------------------------------------------------------------------------------------

    def base_urls(self):
        return [
            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash(),), self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/schema\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('get_schema'), name="api_get_schema"),
            url(r"^(?P<resource_name>%s)/schema%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_schema'), name="api_get_schema"),
            url(r"^(?P<resource_name>%s)/datatables\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('get_datatables'), name="api_get_datatables"),
            url(r"^(?P<resource_name>%s)/(?P<molecule__chembl_id>[Cc][Hh][Ee][Mm][Bb][Ll]\d[\d]*)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<standard_inchi_key>[A-Z]{14}-[A-Z]{10}-[A-Z])%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<molecule__chembl_id>[Cc][Hh][Ee][Mm][Bb][Ll]\d[\d]*)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<standard_inchi_key>[A-Z]{14}-[A-Z]{10}-[A-Z])\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<molecule__chembl_id>[Cc][Hh][Ee][Mm][Bb][Ll]\d[\d]*)$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<standard_inchi_key>[A-Z]{14}-[A-Z]{10}-[A-Z])$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<standard_inchi_key>[A-Z]{14}-[A-Z]{10}-[A-Z])\.(?P<format>svg)$" % MoleculeResource._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<molecule__chembl_id>[Cc][Hh][Ee][Mm][Bb][Ll]\d[\d]*)\.(?P<format>svg)$" % MoleculeResource._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

# ----------------------------------------------------------------------------------------------------------------------

    def prepend_urls(self):
        return []

# ----------------------------------------------------------------------------------------------------------------------

    def error_response(self, request, errors, response_class=None):
        if request.format not in ChEMBLApiSerializer.formats:
            request.format = 'json'
        return super(ImageResource, self).error_response(request, errors, response_class)

# ----------------------------------------------------------------------------------------------------------------------

    def wrap_view(self, view):
        @csrf_exempt
        def wrapper(request, *args, **kwargs):

            if request.method == 'GET':
                kwargs.update(request.GET.dict())

            elif request.method == 'POST':
                if request.META.get('CONTENT_TYPE', 'application/json').startswith(
                        ('multipart/form-data', 'multipart/form-data')):
                    post_arg = request.POST.dict()
                else:
                    post_arg = self.deserialize(request, request.body,
                                                format=request.META.get('CONTENT_TYPE', 'application/json'))
                kwargs.update(post_arg)

            request.format = kwargs.get('format', None)

            if 'molecule__chembl_id' in kwargs and isinstance(kwargs['molecule__chembl_id'], str):
                kwargs['molecule__chembl_id'] = kwargs['molecule__chembl_id'].upper()

            wrapped_view = super(ChemblModelResource, self).wrap_view(view)
            return wrapped_view(request, *args, **kwargs)

        return wrapper

# ----------------------------------------------------------------------------------------------------------------------

    def cached_obj_get(self, **kwargs):
        """
        A version of ``obj_get`` that uses the cache as a means to get
        commonly-accessed data faster.
        """
        get_failed = False
        cache_key = self.generate_cache_key('detail', **kwargs)

        try:
            cached_bundle = self._meta.cache.get(cache_key)
        except Exception:
            cached_bundle = None
            get_failed = True
            self.log.error('Caching get exception', exc_info=True, extra={'kwargs': kwargs, })

        if cached_bundle is None:
            cached_bundle = self.obj_get(**kwargs)
            if not get_failed:
                try:
                    self._meta.cache.set(cache_key, cached_bundle)
                except Exception:
                    self.log.error('Caching set exception', exc_info=True, extra={'kwargs': kwargs, })

        return cached_bundle

# ----------------------------------------------------------------------------------------------------------------------

    def obj_get(self, **kwargs):

        chembl_id = kwargs.get('molecule__chembl_id')
        standard_inchi_key = kwargs.get('standard_inchi_key')

        if not chembl_id and not standard_inchi_key:
            raise BadRequest("ChEMBL ID or standard InChi Key required.")

        filters = dict((k,v) for k,v in list(kwargs.items()) if k in ('molecule__chembl_id','standard_inchi_key'))
        stringified_kwargs = ', '.join(["%s=%s" % (k, v) for k, v in list(filters.items())])

        filters.update({
            'molecule__chembl__entity_type':'COMPOUND',
            'molecule__compoundstructures__isnull': False,
            'molecule__compoundproperties__isnull': False,
        })

        try:
            molfile_list = self.get_object_list(None).filter(**filters).values_list('molfile', flat=True)

            if len(molfile_list) <= 0:
                raise ObjectDoesNotExist("Couldn't find an instance of '%s' which matched '%s'." %
                                                           (self._meta.object_class.__name__, stringified_kwargs))
            elif len(molfile_list) > 1:
                raise MultipleObjectsReturned("More than '%s' matched '%s'." %
                                              (self._meta.object_class.__name__, stringified_kwargs))
        except ValueError:
            raise NotFound("Invalid resource lookup data provided (mismatched type).")

        return molfile_list[0]

# ----------------------------------------------------------------------------------------------------------------------

    def render_image(self, mol, request, **kwargs):
        global BEAKER_CTAB_TO_SVG_URL

        try:
            size = int(kwargs.get("dimensions", 500))
        except ValueError:
            return self.answerBadRequest(request, "Image dimensions supplied are invalid")

        ignoreCoords = kwargs.get("ignoreCoords", False)

        if size < 1 or size > 1500:
            return self.answerBadRequest(request, "Image dimensions supplied are invalid, max value is 500")
        engine = kwargs.get("engine", 'rdkit').lower()
        if engine not in SUPPORTED_ENGINES:
            return self.answerBadRequest(request, "Unsupported engine %s" % engine)

        img_mime_type = None
        mol_img = None

        if engine == 'rdkit':
            img_url = BEAKER_CTAB_TO_SVG_URL
            img_url += '?size={0}'.format(size)
            if ignoreCoords:
                img_url += '&computeCoords=1'
            img_request = requests.post(img_url, data=mol)
            mol_img = img_request.content
            img_mime_type = "image/svg+xml"
        else:
            self.answerBadRequest(request, 'Unsupported rendering engine "{0}"'.format(engine))

        response = HttpResponse(content_type=img_mime_type)
        response.write(mol_img)

        return response

# ----------------------------------------------------------------------------------------------------------------------

    def get_detail(self, request, **kwargs):
        cache_key = self.generate_cache_key('image', **dict({'is_ajax': request.is_ajax()}, **kwargs))
        get_failed = False

        in_cache = False
        start = time.time()
        try:
            ret = self._meta.cache.get(cache_key)
            in_cache = True
        except Exception:
            ret = None
            get_failed = True
            self.log.error('Cashing get exception', exc_info=True, extra=kwargs)

        if ret is None:
            in_cache = False
            ret = self.image_get(request, **kwargs)
            if not get_failed:
                try:
                    self._meta.cache.set(cache_key, ret)
                except Exception:
                    self.log.error('Cashing set exception', exc_info=True, extra=kwargs)

        if WS_DEBUG:
            end = time.time()
            ret['X-ChEMBL-in-cache'] = in_cache
            ret['X-ChEMBL-retrieval-time'] = end - start
        return ret

# ----------------------------------------------------------------------------------------------------------------------

    def image_get(self, request, **kwargs):
        try:
            mol = self.cached_obj_get(**kwargs)
        except ObjectDoesNotExist:
            return http.HttpNotFound()
        except MultipleObjectsReturned:
            return http.HttpMultipleChoices("More than one resource is found at this URI.")

        return self.render_image(mol, request, **kwargs)

# ----------------------------------------------------------------------------------------------------------------------

    def generate_cache_key(self, *args, **kwargs):

        molecule__chembl_id = kwargs.get('molecule__chembl_id', '')
        standard_inchi_key = kwargs.get('standard_inchi_key', '')
        bgColor = kwargs.get('bgColor', '').lower()
        format = kwargs.get('format', 'svg')
        engine = kwargs.get('engine', 'rdkit')
        dimensions = kwargs.get('dimensions', 500)
        ignoreCoords = kwargs.get("ignoreCoords", False)
        is_ajax = kwargs.get("is_ajax", 2)

        # Use a list plus a ``.join()`` because it's faster than concatenation.
        cache_key = "%s:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s" % (self._meta.api_name,
                                                          self._meta.resource_name,
                                                          '|'.join(args),
                                                          str(molecule__chembl_id),
                                                          str(standard_inchi_key),
                                                          str(format),
                                                          str(engine),
                                                          str(dimensions),
                                                          str(ignoreCoords),
                                                          str(is_ajax),
                                                          bgColor)
        return cache_key

# ----------------------------------------------------------------------------------------------------------------------
