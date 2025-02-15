from bank_api.adapters.jwt_auth_adapter import JWTAuthAdapter
from bank_api.adapters.repositories.payment_account_repository import \
    PaymentAccountRepository
from bank_api.adapters.repositories.user_repository import UserRepository
from bank_api.controllers.auth_controller import AuthController
from bank_api.controllers.payment_account_controller import \
    PaymentAccountController
from bank_api.controllers.transfer_controller import TransferController
from bank_api.services.auth_service import AuthService
from bank_api.services.payment_account_service import PaymentAccountService
from bank_api.services.transfer_service import TransferService
from config.database import get_db
from settings import SECRET_KEY

# Adapters
payment_account_repository = PaymentAccountRepository(context_db_session=get_db)
user_repository = UserRepository(context_db_session=get_db)
jwt_adapter = JWTAuthAdapter(secret_key=SECRET_KEY, algorithm='HS256')


# Services
payment_account_service = PaymentAccountService(payment_account_repository=payment_account_repository)
auth_service = AuthService(user_repository=user_repository, auth_adapter=jwt_adapter)
transfer_service = TransferService(payment_account_repository=payment_account_repository)

# Controllers
payment_account_controller = PaymentAccountController(service=payment_account_service)
auth_controller = AuthController(service=auth_service)
transfer_controller = TransferController(service=transfer_service)
