__author__ = 'mnowotka'
from django.conf.urls import url

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from chembl_webservices.api_config import api as webservices

urlpatterns = webservices.urls

@csrf_exempt
def deprecated_target_prediction_request(request):
    return HttpResponse('ERROR: The target prediction endpoint has been removed in ChEMBL 26.\n', status=410)

urlpatterns.append(url(r'^data/target_prediction.*$',
                       deprecated_target_prediction_request, ))
