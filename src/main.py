from fastapi import FastAPI

from bank_api.utils.log import logger
from config import dependencies as deps
from rest import init_middlewares, init_routes
from settings import APPLICATION_NAME


def create_app():
    try:
        app = FastAPI(
            title=APPLICATION_NAME,
            description=f'{APPLICATION_NAME} Service',
        )

        init_middlewares(app)
        init_routes(
            app,
            payment_account_controller=deps.payment_account_controller,
            auth_controller=deps.auth_controller,
            transfer_controller=deps.transfer_controller,
        )

        logger.info(f'{APPLICATION_NAME} App created successfully')

        return app
    except Exception as ex:
        logger.error(f'{ex}')
        raise ex from ex
