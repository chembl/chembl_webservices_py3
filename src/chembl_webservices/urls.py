__author__ = 'mnowotka'
from django.conf.urls import url

from chembl_webservices.api_config import api as webservices
from chembl_webservices.target_predictions_proxy import target_predictions_proxy

urlpatterns = webservices.urls

urlpatterns.append(url(r'^data/target_predictions_proxy$',
                       target_predictions_proxy, ))
