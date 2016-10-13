import os
import tempfile
db_file = tempfile.NamedTemporaryFile()


class Config(object):
    SECRET_KEY = 'secret key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    #BOUNDING_BOX = [44.5963, -70.8620, 44.6111, -70.9626]  # min_lat, max_lon, max_lat, min_lon
    #BOUNDING_BOX = [44.0, -70.1, 44.9, -71.3]  # min_lat, max_lon, max_lat, min_lon really big
    BOUNDING_BOX = [44.5, -70.8, 44.7, -71.0]
    MAPBOX_TOKEN = os.environ.get('MAPBOX_TOKEN')
    MAPBOX_USER = os.environ.get('MAPBOX_USER')


class ProdConfig(Config):
    ENV = 'prod'

    CACHE_TYPE = 'simple'


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_ECHO = True

    CACHE_TYPE = 'null'
    ASSETS_DEBUG = True
    


class TestConfig(Config):
    ENV = 'test'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_file.name
    SQLALCHEMY_ECHO = True

    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False
    BOUNDING_BOX = [44.5963, -70.8620, 44.6111, -70.9626]  # min_lat, max_lon, max_lat, min_lon
