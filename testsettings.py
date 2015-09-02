import django.conf.global_settings as DEFAULT_SETTINGS
import os

BASE_DIR = os.path.dirname(__file__)

SECRET_KEY = 'oxkvjtm'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'mptt',
    'paiji2_forum',
    'paiji2_utils',
)

ROOT_URLCONF = 'testurls'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

LANGUAGE_CODE = 'en'


# html validation (django-html-validator)

HTMLVALIDATOR_ENABLED = True

HTMLVALIDATOR_FAILFAST = True

# try:
#     assert(os.getenv('HOSTNAME') == "lgdubois.rez")
#     HTMLVALIDATOR_VNU_JAR = '~/dev/dist/vnu.jar'
#     print("[html validation] using :" + HTMLVALIDATOR_VNU_JAR)
# except:
HTMLVALIDATOR_VNU_URL = 'https://validator.nu/'
print("[html validation] using :" + HTMLVALIDATOR_VNU_URL)

HTMLVALIDATOR_DUMPDIR = os.path.join(BASE_DIR, 'validation_errors')

HTMLVALIDATOR_OUTPUT = 'file'  # default is 'file'
