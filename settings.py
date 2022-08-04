from os import getenv

ENVIRONMENT = getenv('ENV')

if  getenv('GAE_ENV') == 'standard':
    SQLALCHEMY_DATABASE_URL = 'sqlite:///:memory:'
else:
    SQLALCHEMY_DATABASE_URL = 'sqlite:///db.sqlite3'