from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+5+()*#k#6j$l0noo3^_n%m!2q8)0&yo%ze-k6l0v3=hwx5l@@'


if DEBUG:
   INTERNAL_IPS = ('127.0.0.1', 'localhost',)
   MIDDLEWARE += [
       'debug_toolbar.middleware.DebugToolbarMiddleware',
   ]

   INSTALLED_APPS += (
       'debug_toolbar',
   )

   DEBUG_TOOLBAR_PANELS = [
       
       'debug_toolbar.panels.timer.TimerPanel',
       'debug_toolbar.panels.settings.SettingsPanel',
       'debug_toolbar.panels.headers.HeadersPanel',
       'debug_toolbar.panels.request.RequestPanel',
       'debug_toolbar.panels.sql.SQLPanel',
       'debug_toolbar.panels.staticfiles.StaticFilesPanel',
       'debug_toolbar.panels.templates.TemplatesPanel',
       'debug_toolbar.panels.cache.CachePanel',
       'debug_toolbar.panels.signals.SignalsPanel',
       'debug_toolbar.panels.logging.LoggingPanel',
       'debug_toolbar.panels.redirects.RedirectsPanel',
   ]

   DEBUG_TOOLBAR_CONFIG = {
       'INTERCEPT_REDIRECTS': False,
   }


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass

ALLOWED_HOSTS = ['192.168.1.35', 'localhost']

#from .data import *
