__author__ = 'mnowotka'

from django.http import HttpResponse
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import RequestFactory
from collections import OrderedDict
import json

#-----------------------------------------------------------------------------------------------------------------------

def generate_spore_endpoint(request, api, name, version):

    envelope = {
        "expected_status": [200],
        "version": version,
        "name": name,
        "methods": OrderedDict()
    }

    registry = api._registry
    factory = RequestFactory()

    for resource_name, resource in sorted(registry.items()):
        #print 'analysing ' + resource_name + ' resource'
        try:
            schema_url = reverse('api_get_schema', kwargs={'api_name':api.api_name, 'resource_name': resource_name})
        except NoReverseMatch:
            print 'No schema for ' + resource_name + ' resource'
            continue
        formats = resource._meta.serializer.formats
        required_params_dict = None
        if hasattr(resource._meta, 'required_params'):
            required_params_dict = resource._meta.required_params
        description_dict = {}
        if hasattr(resource._meta, 'description'):
            description_dict = resource._meta.description
        request = factory.get(schema_url)
        request.format = 'json'
        schema = resource.get_schema(request)
        schema_dict = json.loads(schema.content)
        allowed_detail_http_methods = schema_dict['allowed_detail_http_methods']
        allowed_list_http_methods = schema_dict['allowed_list_http_methods']
        available_methods = [url.name for url in resource.urls]

        #print 'available_methods:'
        #print available_methods

        for verb in ['get', 'post']:
            for type in ['api_dispatch_list', 'api_dispatch_detail', 'api_get_multiple', 'api_get_search']:
                if type not in available_methods:
                    continue
                if type in ('api_dispatch_list','api_get_multiple', 'api_get_search') and verb not in allowed_list_http_methods:
                    continue
                elif type == 'api_dispatch_detail' and verb not in allowed_detail_http_methods:
                    continue
                method_name = verb.upper() + '_' + resource_name + '_' + type
                canonical_url = schema_url[:schema_url.find('/schema') + 1]
                if type == 'api_dispatch_list':
                    description = description_dict.get(type, "Retrieve " + resource_name + " object list.")
                    required_params = []
                elif type == 'api_dispatch_detail':
                    canonical_url += ':ID'
                    description = description_dict.get(type, "Retrieve single " + resource_name + " object details by ID.")
                    required_params = ['ID']
                elif type == 'api_get_multiple':
                    canonical_url += 'set/:IDs_list'
                    description = description_dict.get(type, "Retrieve multiple " + resource_name + " objects by IDs.")
                    required_params = ['IDs_list']
                elif type == 'api_get_search':
                    canonical_url += 'search?q=:query'
                    description = description_dict.get(type, "Search " + resource_name + " using query string.")
                    required_params = ['query']
                if required_params_dict:
                    required_params = required_params_dict.get(type, required_params)
                    canonical_url = canonical_url[:canonical_url.find(':')] + '/'.join([':' + x for x in required_params])
                method_data = {
                    "method" : verb.upper(),
                    "resource_name": resource_name,
                    "schema": schema_url,
                    "collection_name": resource._meta.collection_name,
                    "default_format": resource._meta.default_format,
                    "description": description,
                    "path" : canonical_url,
                    "required_params": required_params,
                    "formats": formats
                }
                envelope["methods"][method_name] = method_data

    return HttpResponse(json.dumps(envelope), content_type="application/json")

#-----------------------------------------------------------------------------------------------------------------------
