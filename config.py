import os

class BaseConfig(object):
  DEBUG = False
  SECRET_KEY = '\xbf\xb0\x11\xb1\xcd\xf9\xba\x8bp\x0c...'

class TestConfig(BaseConfig):
  DEBUG = True
  BASE_DIR = os.path.abspath(os.path.dirname(__file__))
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')

class DevelopmentConfig(BaseConfig):
  BASE_DIR = os.path.abspath(os.path.dirname(__file__))
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
  DEBUG = True

class ProductionConfig(BaseConfig):
  BASE_DIR = os.path.abspath(os.path.dirname(__file__))
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
  DEBUG = False
