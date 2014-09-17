# Django settings for mixkey project.

import os, sys
BASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'mixkey',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1


LANGUAGE_CODE = 'en'

gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
    ('th', gettext('Thai')),
)

LOCALE_PATHS = (
    os.path.join(BASE_PATH, 'locale'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True



# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

MEDIA_ROOT = os.path.join(BASE_PATH, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_PATH, 'sitestatic/')
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_PATH, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '(-4%mvc)#ke+2mjkeue6!g%b2!(0+*9a=(h9f#4968x-jg$h3#'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'domain.middleware.ProjectMiddleware',
    'domain.middleware.ForceInEnglish',
    
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    
    'mixkey.context_processors.site_information',
)

ROOT_URLCONF = 'mixkey.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mixkey.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_PATH, 'templates'),
)

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mixkey.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    
    # Libs
    'kombu.transport.django',
    'djcelery',
    'djsupervisor',
    'daterange_filter',
    'south',
    'debug_toolbar',
    
    # Project
    'domain',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Celery ###############################################################################################################

import djcelery
djcelery.setup_loader()

BROKER_BACKEND = "djkombu.transport.DatabaseTransport"
BROKER_URL = 'django://'

CELERY_IMPORTS = ("domain.tasks", )

from datetime import timedelta
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    # ###### RUN EVERYDAY
    'runs-everyday': {
        'task': 'domain.tasks.send_daily',
        'schedule': crontab(hour=4, minute=0),
    },
}

# TWILIO ###############################################################################################################
TWILIO_SEND_SMS    = True
TWILIO_ACCOUNT_SID = 'REPLACE ME'
TWILIO_AUTH_TOKEN  = 'REPLACE ME'
TWILIO_FROM_NUMBER = 'REPLACE ME'

PREV_DATA_BUFFER_TIME = 20 # miniutes
MAX_REPEAT_ALERT = 5

DETECT_SENSOR_LOST_TIME = 30 # miniutes
DETECT_SENSOR_LOST_TEL_LIST = '+66897070170|panudate@opendream.co.th,+66897753337|patipat@opendream.co.th,+66842226566|paskorn@eng.cmu.ac.th,+66804986837|zerox.lp@gmail.com'

# Email Settings #######################################################################################################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 25

EMAIL_SUBJECT_PREFIX = 'TELEMETRY STATION'
EMAIL_DOMAIN_NAME = 'mixkey-data.opendreamlabs.com'

EMAIL_ADDRESS_NO_REPLY = '%s <webmaster@%s>' % (EMAIL_SUBJECT_PREFIX, EMAIL_DOMAIN_NAME)

CACHES = {
    'default': {
        #'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 60*10
    },
    'resources': {
        #'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 60*10
    }
}

# Level Settings #######################################################################################################

BATTERY_RED_LEVEL = 10.5
BATTERY_YELLOW_LEVEL = 11.5


# Override Settings ###########################################################
try:
    from settings_local import *
except ImportError:
    pass


# TESTING #####################################################################
if 'test' in sys.argv:
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
    MEDIA_ROOT = os.path.join(BASE_PATH, 'test_media')
    MEDIA_URL = '/test_media/'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
