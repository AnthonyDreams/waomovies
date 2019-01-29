"""
Django settings for Wao project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = 'j$z5qv+cug3pd8p6#jnbj+mdn$0x#fonrlk#=&f*1f0_e)=&yt'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#ALLOWED_HOSTS = ['127.0.0.1','wmoviestest.herokuapp.com', "0.0.0.0"]
ALLOWED_HOSTS = ['wmoviestest.herokuapp.com']

NOTICIAS = True
SERIES = False

# Application definition

INSTALLED_APPS = [
	'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.peliculas',
    'apps.series',
    'apps.usuarios',
    'apps.comentarios',
    'apps.vermas_tarde',
    'apps.notificaciones',
    'apps.footer',
    'multiselectfield',
    'apps.contacto',
    'apps.dashboard',
    'apps.news',
    'timedeltatemplatefilter',
]

AUTH_USER_MODEL = 'usuarios.Usuario'

MOVIES_DEL_WEB = 'peliculas.Peliculas'
ARTICLES_DE_WEB = 'news.Article'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
]

ROOT_URLCONF = 'Wao.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],

            'libraries':{
            	'my_templatetag': 'apps.peliculas.templatetags.tags',

            }
        },
    },
]

WSGI_APPLICATION = 'Wao.wsgi.application'

#ASGI_APPLICATION = 'Wao.routing.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'database',
        'USER': 'postgres',
        'PASSWORD': 'a253035253035',
        'HOST': 'localhost',
        'PORT': 5432,

    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'waosoporte@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

DEB = True

if DEB:
	MEDIA_URL = '/media/'

	MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

	# Static files (CSS, JavaScript, Images)
	# https://docs.djangoproject.com/en/2.0/howto/static-files/

	STATIC_URL = '/static/'
	STATIC_DIRS = 'static'
	STATICFILES_DIRS = [
	    STATIC_DIRS,

	]
	STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

else:
	
	STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
	DEFAULT_FILE_STORAGE = 'Wao.storage_backends.PublicMediaStorage'

	#S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
	#STATIC_URL = 'http://' + S3_BUCKET_NAME + '.s3.amazonaws.com/'
	#AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
	#AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
	STATIC_DIRS = 'static'
	STATICFILES_DIRS = [
	    STATIC_DIRS,

	]
	AWS_ACCESS_KEY_ID = 'AKIAJ4IOBCQM32A5LVWQ'
	AWS_SECRET_ACCESS_KEY = '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'
	AWS_STORAGE_BUCKET_NAME = 'waomovies'
	AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
	AWS_HEADERS = {
    'Expires': 'Thu, 15 Apr 2010 20:00:00 GMT',
    'Cache-Control': 'max-age=86400',
}
	AWS_LOCATION = 'static'
	AWS_DEFAULT_ACL = "public-read"
	AWS_CLOUDFRONT_DOMAIN = "d3mp3oxoqwxddf.cloudfront.net"
	CLOUDFRONT_DOMAIN = "d11nqwgsnjp6i8.cloudfront.net"
	AWS_CLOUDFRONT_ID = "E1VWKMT8Y4CWEQ"


	AWS_PRELOAD_METADATA = True
	STATIC_URL = 'https://%s/%s/' % (CLOUDFRONT_DOMAIN, AWS_LOCATION)
	STATICFILES_STORAGE = 'Wao.storage_backends.StaticStorage'
	ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
	AWS_PUBLIC_MEDIA_LOCATION = 'media'
	MEDIA_URL = '//%s/%s/' % (AWS_CLOUDFRONT_DOMAIN, AWS_PUBLIC_MEDIA_LOCATION)

	DEFAULT_FILE_STORAGE = 'Wao.storage_backends.PublicMediaStorage'
	AWS_DEFAULT_ACL = None



channell = False
if channell:
	if DEB:
		CHANNEL_LAYERS = {
		    'default': {
		        'BACKEND': 'channels_redis.core.RedisChannelLayer',
		        'CONFIG': {
		            'hosts': [('localhost', 6379)],
		        },
		    }
		}
	else:
		CHANNEL_LAYERS = {
		    'default': {
		        'BACKEND': 'channels_redis.core.RedisChannelLayer',
		        'CONFIG': {
		            'hosts': [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
		        },
		    }
		}