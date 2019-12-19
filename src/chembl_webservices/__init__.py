__author__ = 'mnowotka'

try:
    __version__ = __import__('pkg_resources').get_distribution('chembl_webservices').version
except Exception as e:
    __version__ = 'development'

default_app_config = 'chembl_webservices.api_config.WebServicesConfig'
