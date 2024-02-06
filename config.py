import os

HOST_ADD = os.environ.get('HOST_ADD', 'localhost')
HOST_PORT = os.environ.get('HOST_PORT', 8000)

DB_NAME = os.environ.get('DB_NAME', 'oauth_postgres')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASS', 'postgres')

DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

SECRET_KEY = os.environ.get('SECRET_KEY', '123')
ALGORITHM = os.environ.get('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE = os.environ.get('ACCESS_TOKEN_EXPIRE', 60*60)  # one hour
