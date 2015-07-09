import os

from django.conf import global_settings
from django.conf import settings

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

if not settings.configured and not os.environ.get('DJANGO_SETTINGS_MODULE'):
  settings.configure(
    INSTALLED_APPS=[
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'djpipelinedb'
    ],
    DATABASES={
      'default': {
        'NAME': 'usmanm',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'usmanm',
        'HOST': 'localhost',
        'PORT': '6543'
      }
    },
    MIDDLEWARE_CLASSES=global_settings.MIDDLEWARE_CLASSES + (
      'djpipelinedb.middleware.RequestLoggingMiddleware',
    ),
    ROOT_URLCONF='djpipelinedb.tests.urls',
    FIXTURES_DIRS=(
      os.path.join(SITE_ROOT, 'djpipelinedb/tests/fixtures'),
    ),
    DEBUG=False
  )
