import os

ENV = os.getenv('FLASK_ENV')
DEBUG = ENV == 'development'
