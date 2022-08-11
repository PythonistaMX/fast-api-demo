from os import getenv

TESTING = True
ENVIRONMENT = getenv('ENV')
DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')

if  getenv('GAE_ENV') == 'standard':
    SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///db.sqlite3'
else:
    SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///db.sqlite3'