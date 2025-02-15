from decouple import config

from bank_api.utils.enviroment import EnvironmentSet

APPLICATION_NAME = config('APPLICATION_NAME', default='Bank Api')
ENVIRONMENT = config('ENVIRONMENT', default=EnvironmentSet.DEVELOPMENT)
SECRET_KEY = config('SECRET_KEY', default='4a8ff935-b592-43a1-b8dd-b3d070da5d88')

DATABASE_URL = config(
    'DATABASE_URL',
    default='postgresql+asyncpg://postgres:postgres@zpy-enterprise-communication-partner:5432/zpy-enterprise-communication-partner',
)
