LOCAL_SETTINGS = True
from django.conf import settings
from settings import *

# define environment
STAGE_NAME = 'PROD' # either PROD or DEV

# debugging changes according to environment configuration
if STAGE_NAME == 'DEV':
    DEBUG = True
else :
    DEBUG = False

TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',                   # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                                             # Or path to database file if using sqlite3.
        'USER': '',                                             # Not used with sqlite3.
        'PASSWORD': '',                                         # Not used with sqlite3.
        'HOST': '',                                             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                             # Set to empty string for default. Not used with sqlite3.
    }    
}
 
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_URL = 'http://127.0.0.1:8000/media/'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'



PAYPAL_SANDBOX_MODE = True
PAYPAL_CURRENCY = 'USD'
PAYPAL_HEADER_IMG = ''
PAYPAL_HEADER_BACK_COLOR = '#dddaaa'
PAYPAL_HEADER_BORDER_COLOR = '#ffffff'
PAYPAL_API_USERNAME = ''
PAYPAL_API_PASSWORD = ''
PAYPAL_API_SIGNATURE = ''