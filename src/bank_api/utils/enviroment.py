from enum import StrEnum


class EnvironmentSet(StrEnum):
    PRODUCTION = 'production'
    DEVELOPMENT = 'development'
    SANDBOX = 'sandbox'
    STAGING = 'staging'
