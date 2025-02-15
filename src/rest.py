from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from bank_api.controllers.auth_controller import AuthController
from bank_api.controllers.payment_account_controller import \
    PaymentAccountController
from bank_api.controllers.transfer_controller import TransferController
from bank_api.exceptions.base_exception import BaseException


def init_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def init_routes(
    app: FastAPI,
    payment_account_controller: PaymentAccountController,
    auth_controller: AuthController,
    transfer_controller: TransferController
):
    app.include_router(
        payment_account_controller.router,
        tags=['PaymentAccount'],
        prefix='/account',
    )

    app.include_router(
        auth_controller.router,
        tags=['Auth'],
        prefix='/auth',
    )

    app.include_router(
        transfer_controller.router,
        tags=['Transfer'],
        prefix='/transfer',
    )

    @app.get('/', tags=['Health Check'])
    async def health_check():
        return {'message': 'OK'}

    @app.exception_handler(BaseException)
    async def common_exception_handler(request: Request, error: BaseException):
        print(f"Código de erro: {error.code} - Mensagem: {error.to_dict()}")
        return JSONResponse(error.to_dict(), status_code=error.code)
