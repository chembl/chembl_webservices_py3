__author__ = 'mnowotka'

import time
import requests
import urllib.parse
from tastypie import http
from django.http import HttpResponse
from tastypie import fields
from chembl_webservices.core.resource import ChemblModelResource
from chembl_webservices.core.meta import ChemblResourceMeta
from chembl_webservices.core.serialization import ChEMBLApiSerializer
from chembl_webservices.core.utils import NUMBER_FILTERS, CHAR_FILTERS
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings
from django.db.models import Prefetch

from chembl_core_model.models import CompoundStructuralAlerts
from chembl_core_model.models import MoleculeDictionary
from chembl_core_model.models import StructuralAlerts

from chembl_core_model.models import StructuralAlertSets

from chembl_webservices.core.fields import monkeypatch_tastypie_field
monkeypatch_tastypie_field()

BEAKER_HIGHLIGHT_SVG_URL = settings.BEAKER_URL + '/highlightCtabFragmentSvg'

# ----------------------------------------------------------------------------------------------------------------------


class StructuralAlertSetsResource(ChemblModelResource):

    class Meta(ChemblResourceMeta):
        queryset = StructuralAlertSets.objects.all()
        resource_name = 'structural_alert_set'
        collection_name = 'structural_alert_sets'
        serializer = ChEMBLApiSerializer(resource_name, {collection_name: resource_name})

        fields = (
            'set_name',
            'priority',
        )
        filtering = {
            'set_name': CHAR_FILTERS,
            'priority': NUMBER_FILTERS,
        }

        ordering = [field for field in list(filtering.keys()) if not ('comment' in field or 'description' in field or
                                                                'canonical_smiles' in field)]

# ----------------------------------------------------------------------------------------------------------------------


class StructuralAlertsResource(ChemblModelResource):

    alert_set = fields.ForeignKey('chembl_webservices.resources.structural_alerts.StructuralAlertSetsResource',
                                  'alertset', full=True, null=True, blank=True)

    class Meta(ChemblResourceMeta):
        queryset = StructuralAlerts.objects.all()
        resource_name = 'structural_alert'
        collection_name = 'structural_alerts'
        serializer = ChEMBLApiSerializer(resource_name, {collection_name: resource_name})
        prefetch_related = [Prefetch('alertset')]

        fields = (
            'alert_id',
            'alert_name',
            'smarts',
        )

        filtering = {
            'alert_id': NUMBER_FILTERS,
            'alert_name': CHAR_FILTERS,
            'smarts': CHAR_FILTERS,
            'alert_set': ALL_WITH_RELATIONS,
        }

        ordering = [field for field in list(filtering.keys()) if not ('comment' in field or 'description' in field or
                                                                'canonical_smiles' in field)]

# ----------------------------------------------------------------------------------------------------------------------


class ImageAwareSerializer(ChEMBLApiSerializer):

    formats = ['xml', 'json', 'jsonp', 'yaml', 'svg']

    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'urlencode': 'application/x-www-form-urlencoded',
        'svg': 'image/svg+xml',
    }

# ----------------------------------------------------------------------------------------------------------------------


class CompoundStructuralAlertsResource(ChemblModelResource):

    molecule_chembl_id = fields.CharField('molecule__chembl_id')
    alert = fields.ForeignKey('chembl_webservices.resources.structural_alerts.StructuralAlertsResource',
                              'alert', full=True, null=True, blank=True)

    class Meta(ChemblResourceMeta):
        queryset = CompoundStructuralAlerts.objects.all()
        resource_name = 'compound_structural_alert'
        collection_name = 'compound_structural_alerts'
        serializer = ImageAwareSerializer(resource_name, {collection_name: resource_name})
        prefetch_related = [
            Prefetch('alert'),
            Prefetch('alert__alertset'),
            Prefetch('molecule', queryset=MoleculeDictionary.objects.only('chembl')),
        ]
        fields = (
            'cpd_str_alert_id'
        )
        filtering = {
            'alert': ALL_WITH_RELATIONS,
            'cpd_str_alert_id': ALL,
            'molecule_chembl_id': ALL,
        }
        ordering = [field for field in list(filtering.keys()) if not ('comment' in field or 'description' in field or
                                                                'canonical_smiles' in field)]

# ----------------------------------------------------------------------------------------------------------------------

    def get_detail_impl(self, request, base_bundle, **kwargs):
        try:
            obj, in_cache = self.cached_obj_get(bundle=base_bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return http.HttpNotFound()
        except MultipleObjectsReturned:
            return http.HttpMultipleChoices("More than one resource is found at this URI.")

        frmt = request.format

        if frmt == 'png':
            self.answerBadRequest(request, 'PNG format has been deprecated, please use SVG.')

        if not frmt:
            if 'HTTP_ACCEPT' in request.META:
                if request.META['HTTP_ACCEPT'] == 'image/svg' or request.META['HTTP_ACCEPT'] == 'image/svg+xml':
                    frmt = 'svg'
                request.format = frmt

        if frmt in ['svg']:
            get_failed = False
            cache_key = self.generate_cache_key('image', **dict({'is_ajax': request.is_ajax()}, **kwargs))
            ret = None
            try:
                ret = self._meta.cache.get(cache_key)
                in_cache = True
            except Exception:
                ret = None
                get_failed = True
                self.log.error('Cashing get exception', exc_info=True, extra=kwargs)

            if ret is None:
                in_cache = False
                ret = self.render_image(obj, request, **kwargs)
                if not get_failed:
                    try:
                        self._meta.cache.set(cache_key, ret)
                    except Exception:
                        self.log.error('Cashing set exception', exc_info=True, extra=kwargs)
            return ret, in_cache

        else:
            bundle = self.build_bundle(obj=obj, request=request)
            bundle = self.full_dehydrate(bundle, **kwargs)
            bundle = self.alter_detail_data_to_serialize(request, bundle)
            return bundle, in_cache

# ----------------------------------------------------------------------------------------------------------------------

    def render_image(self, obj, request, **kwargs):
        global BEAKER_HIGHLIGHT_SVG_URL

        req_format = getattr(request, 'format',  'svg')
        try:
            size = int(kwargs.get("dimensions", 500))
        except ValueError:
            return self.answerBadRequest(request, "Image dimensions supplied are invalid")
        ignoreCoords = kwargs.get("ignoreCoords", False)

        if size < 1 or size > 1500:
            return self.answerBadRequest(request, "Image dimensions supplied are invalid, max value is 500")
        engine = kwargs.get("engine", 'rdkit').lower()

        img_mime_type = None
        highlighted_mol_img = None

        if engine == 'rdkit' and req_format == 'svg':
            img_url = BEAKER_HIGHLIGHT_SVG_URL
            img_url += '?size={0}&force=1'.format(size)
            if ignoreCoords:
                img_url += '&computeCoords=1'

            molstring = obj.molecule.compoundstructures.molfile
            smarts = urllib.parse.quote(obj.alert.smarts)

            img_url += '&smarts={0}'.format(smarts)

            img_request = requests.post(img_url, data=molstring)
            if img_request.status_code != 200:
                self.answerBadRequest(request, 'Beaker at {0} could not fulfill your request for smarts: {1}\nSDF:{2}\n'
                                      .format(BEAKER_HIGHLIGHT_SVG_URL, smarts, molstring))

            highlighted_mol_img = img_request.content
            img_mime_type = "image/svg+xml"
        else:
            self.answerBadRequest(request, 'Unsupported rendering engine "{0}" or format "{1}"'
                                  .format(engine, req_format))

        response = HttpResponse(content_type=img_mime_type)
        response.write(highlighted_mol_img)

        return response

# ----------------------------------------------------------------------------------------------------------------------

    def _get_cache_args(self, *args, **kwargs):
        cache_ordered_dict = super(CompoundStructuralAlertsResource, self)._get_cache_args(*args, **kwargs)

        cache_ordered_dict['format'] = str(kwargs.get('format', 'svg'))
        cache_ordered_dict['engine'] = str(kwargs.get('engine', 'rdkit'))
        cache_ordered_dict['dimensions'] = str(kwargs.get('dimensions', 500))
        cache_ordered_dict['ignoreCoords'] = str(kwargs.get("ignoreCoords", False))
        cache_ordered_dict['is_ajax'] = str(kwargs.get("is_ajax", 2))
        cache_ordered_dict['bgColor'] = kwargs.get('bgColor', '').lower()

        return cache_ordered_dict

# ----------------------------------------------------------------------------------------------------------------------

    def response(self, f):

        def get_something(request, **kwargs):
            start = time.time()
            basic_bundle = self.build_bundle(request=request)

            ret = f(request, basic_bundle, **kwargs)
            if isinstance(ret, tuple) and len(ret) == 2:
                bundle, in_cache = ret
            else:
                return ret

            if not type(bundle) == HttpResponse:
                res = self.create_response(request, bundle)
            else:
                res = bundle

            if settings.DEBUG:
                end = time.time()
                res['X-ChEMBL-in-cache'] = in_cache
                res['X-ChEMBL-retrieval-time'] = end - start
            return res

        return get_something

# ----------------------------------------------------------------------------------------------------------------------
