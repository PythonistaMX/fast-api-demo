from os import getenv

TESTING = True
ENVIRONMENT = getenv('ENV')

if  getenv('GAE_ENV') == 'standard':
    SQLALCHEMY_DATABASE_URL = 'sqlite:///db.sqlite3'
else:
    '''
    SQLALCHEMY_DATABASE_URL = 'sqlite:///:memory:'
    '''
    SQLALCHEMY_DATABASE_URL = 'sqlite:///db.sqlite3'