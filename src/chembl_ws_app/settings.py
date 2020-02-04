import os, sys
import hashlib
import traceback
import pathlib
import requests

# Load ENV file if defined ---------------------------------------------------------------------------------------------

ENV_FILE_LOADED = int(os.environ.get('CHEMBL_WS_PY3_ENV_LOADED', 0))

ENV_FILE = os.environ.get('CHEMBL_WS_PY3_ENV')
if ENV_FILE and not ENV_FILE_LOADED:
    if os.path.exists(ENV_FILE) and os.path.isfile(ENV_FILE):
        # noinspection PyBroadException
        try:
            with open(ENV_FILE, 'r') as env_file:
                env_lines = env_file.readlines()
                for line in env_lines:
                    line = line.strip()
                    if line[0] != '#':
                        env_setting = line.split('=')
                        if len(env_setting) < 2:
                            print('WARNING ENV VARIABLE LINE IGNORED: {0}'.format(line), file=sys.stderr)
                            continue
                        os.environ.setdefault(env_setting[0], '='.join(env_setting[1:]))
                        print('ENV VARIABLE LOADED: {0} => {1}'.format(env_setting[0], os.environ.get(env_setting[0])))
                os.environ.setdefault('CHEMBL_WS_PY3_ENV_LOADED', '1')
        except:
            print('ENV FILE ERROR - - -'.format(ENV_FILE), file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            print('ERROR: Environment file at {0} could not be read.'.format(ENV_FILE), file=sys.stderr)
            print('ENV FILE ERROR - - -'.format(ENV_FILE), file=sys.stderr)
    else:
        print('ENV FILE ERROR - - -'.format(ENV_FILE), file=sys.stderr)
        print('ERROR: Environment file at {0} does not exist or is not a file.'.format(ENV_FILE), file=sys.stderr)
        print('ENV FILE ERROR - - -'.format(ENV_FILE), file=sys.stderr)


# Validate required ENV variables --------------------------------------------------------------------------------------

REQUIRED_ENVIRONMENT_VARIABLES=[
    'SECRET_KEY',
    'DEBUG',
    'ADMIN_NAME',
    'ADMIN_EMAIL',
    'FPSIM2_FILE_URL',
    'FPSIM2_FILE_PATH',
    'SQL_DATABASE',
    'SQL_USER',
    'SQL_PASSWORD',
    'SQL_HOST',
    'SQL_PORT',
    'MONGO_CACHE_LOCATION',
    'MONGO_CACHE_HOSTS',
    'MONGO_CACHE_RSNAME',
    'MONGO_CACHE_AUTH_DATABASE',
    'MONGO_CACHE_DATABASE',
    'MONGO_CACHE_USER',
    'MONGO_CACHE_PASSWORD',
]

missing_required_vars = []
for env_var_i in REQUIRED_ENVIRONMENT_VARIABLES:
    var_val = os.environ.get(env_var_i)
    if not var_val:
        missing_required_vars.append(env_var_i)

if missing_required_vars:
    print('CONFIG ERROR: missing settings variables {0}.'.format(', '.join(missing_required_vars)), file=sys.stderr)
    print('-----------------------------------------------------------------------------------------', file=sys.stderr)
    print('You can use CHEMBL_WS_PY3_ENV environment variable to define an ENVIRONMENT file to load.', file=sys.stderr)
    print('-----------------------------------------------------------------------------------------', file=sys.stderr)
    sys.exit(1)


TEST_RUNNER = 'django.test.runner.DiscoverRunner'

DEBUG_TOOLBAR_PATCH_SETTINGS = False

SERVER_BASE_PATH = '/chembl/api'

WS_NAME = 'data'
WS_DEBUG = True

DJANGO_SERVER_HOST = 'localhost'
DJANGO_SERVER_PORT = 8000

CTAB_COLUMN='m'

ALLOWED_HOSTS = '*'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = (
        'x-requested-with',
        'content-type',
        'accept',
        'origin',
        'authorization',
        'x-csrftoken',
        'x-http-method-override',
    )


TASTYPIE_DOC_API = 'chembl_webservices.api_config.api'
TASTYPIE_DOC_NAME = 'ChEMBL web services API live documentation'
TASTYPIE_ALLOW_MISSING_SLASH = True
TASTYPIE_CANNED_ERROR = "An internal server error occurred. Please contact ChEMBL help."

API_INFO = {
  "title": "ChEMBL REST API",
  "description": "The official ChEMBL RESTful API",
  "termsOfServiceUrl": "https://www.ebi.ac.uk/chembl/ws",
  "contact": "chembl-help@ebi.ac.uk",
  "license": "Apache 2.0",
  "licenseUrl": "http://www.apache.org/licenses/LICENSE-2.0.html"
}

DEBUG = int(os.environ.get('DEBUG', default=0))

ADMINS = (
    (os.environ.get('ADMIN_NAME'), os.environ.get('ADMIN_EMAIL')),
)

MANAGERS = ADMINS

# Validate required ENV variables --------------------------------------------------------------------------------------

FPSIM2_FILE_URL = os.environ.get('FPSIM2_FILE_URL')
FPSIM2_FILE_PATH = os.environ.get('FPSIM2_FILE_PATH')

if not os.path.exists(FPSIM2_FILE_PATH):
    # noinspection PyBroadException
    try:
        pathlib.Path(FPSIM2_FILE_PATH).touch()
        download_req = requests.get(FPSIM2_FILE_URL)
        if download_req.status_code != 200:
            raise Exception('DOWNLOAD ERROR: STATUS: {0} URL: {1}'.format(download_req.status_code, FPSIM2_FILE_URL))
        with open(FPSIM2_FILE_PATH, 'wb') as download_file:
            download_file.write(download_req.content)
    except:
        print('- FPSIM2 FILE DOWNLOAD ERROR -------', file=sys.stderr)
        traceback.print_exc()
        print('- END FPSIM2 FILE DOWNLOAD ERROR ---', file=sys.stderr)
        try:
            pathlib.Path(FPSIM2_FILE_PATH).unlink()
        except:
            print('- FPSIM2 FILE CLEAN ERROR -------', file=sys.stderr)
            traceback.print_exc()
            print('- END FPSIM2 FILE CLEAN ERROR ---', file=sys.stderr)
        sys.exit(1)


# SQL Database connection ----------------------------------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('SQL_DATABASE'),
        'USER': os.environ.get('SQL_USER'),
        'PASSWORD': os.environ.get('SQL_PASSWORD'),
        'HOST': os.environ.get('SQL_HOST'),
        'PORT': os.environ.get('SQL_PORT'),
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = SERVER_BASE_PATH + '/' + WS_NAME + '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get("SECRET_KEY")

# INSTALLED APPS and MIDDLEWARES ---------------------------------------------------------------------------------------

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'tastypie',
    'haystack',
    'chembl_core_db',
    'chembl_core_model',
    'chembl_webservices',
    'tastypie_spore_docs',
    'corsheaders',
)

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    # 'chembl_webservices.middleware.SqlPrintingMiddleware',

    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

# Templates Settings ---------------------------------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

# ----------------------------------------------------------------------------------------------------------------------

ROOT_URLCONF = 'chembl_ws_app.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'chembl_ws_app.wsgi.application'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://ves-hx-58.ebi.ac.uk:7777/solr/#/',
        # 'URL': 'http://ves-hx-58.ebi.ac.uk:8080/solr/#/',
        'TIMEOUT': 1000,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 1000,
        'SILENTLY_FAIL': False,
    },
}

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}


# Mongo Cache Settings -------------------------------------------------------------------------------------------------

from pymongo.read_preferences import ReadPreference
import pymongo

def ws_make_key(key, key_prefix, version):
    return hashlib.md5(('{0}:{1}:{2}'.format(key_prefix, version, key)).encode('utf-8')).hexdigest()

CACHES = {
    'default': {
        'BACKEND': 'chembl_core_db.cache.backends.MongoDBCache.MongoDBCache',
        'LOCATION': os.environ.get('MONGO_CACHE_LOCATION'),
        'TIMEOUT': 30000000,
        'KEY_FUNCTION' : ws_make_key,
        'OPTIONS': {
            'HOST': os.environ.get('MONGO_CACHE_HOSTS').split(' '),
            'RSNAME': os.environ.get('MONGO_CACHE_RSNAME'),
            'MAX_ENTRIES': 100000000000,
            'AUTH_DATABASE': os.environ.get('MONGO_CACHE_AUTH_DATABASE'),
            'DATABASE': os.environ.get('MONGO_CACHE_DATABASE'),
            'USER': os.environ.get('MONGO_CACHE_USER'),
            'PASSWORD': os.environ.get('MONGO_CACHE_PASSWORD'),
            'SOCKET_TIMEOUT_MS': 4000,
            'CONNECT_TIMEOUT_MS': 2000,
            'SERVER_SELECTION_TIMEOUT_MS': 2000,
            'MAX_TIME_MS': 1000,
            'COMPRESSION_LEVEL': 6,
            'COMPRESSION': True,
            'READ_PREFERENCE': ReadPreference.SECONDARY_PREFERRED,
            'INDEXES': [
                {
                    'NAME': 'resource_search',
                    'INDEX_DESCRIPTION': [
                        ('resource_name', pymongo.ASCENDING),
                        ('offset', pymongo.ASCENDING),
                        ('limit', pymongo.ASCENDING)
                    ]
                },
                {
                    'NAME': 'url_search',
                    'INDEX_DESCRIPTION': [
                        ('url', pymongo.ASCENDING)
                    ]
                }
            ]
        }
    }
}

CACHE_MIDDLEWARE_SECONDS = 3000000
