from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class StaticStorage(S3Boto3Storage):

    location = settings.AWS_LOCATION
    def __init__(self, *args, **kwargs):
    	kwargs['custom_domain'] = settings.CLOUDFRONT_DOMAIN
    	super(StaticStorage, self).__init__(*args, **kwargs)

class PublicMediaStorage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = False

    def __init__(self, *args, **kwargs):
    	kwargs['custom_domain'] = settings.AWS_CLOUDFRONT_DOMAIN
    	super(PublicMediaStorage, self).__init__(*args, **kwargs)
