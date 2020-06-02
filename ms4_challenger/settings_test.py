from .settings import *

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
SECRET_KEY = "abc123"