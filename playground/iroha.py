import typing
import os

from iroha import Iroha, IrohaGrpc, IrohaCrypto

ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@test')
IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', 'node')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
ADMIN_PRIVATE_KEY = os.getenv('ADMIN_PRIVATE_KEY', '4148a3308e04975baa77ad2b5f4ac70f250506cf6cf388d3963ade2c68e5b2ad')

net = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR, IROHA_PORT))

def init_client(account_id: str) -> Iroha:
    return Iroha(account_id)

admin = init_client(ADMIN_ACCOUNT_ID)

class IrohaException(Exception):
    def __init__(
        self,
        message: str,
        *,
        reason: typing.Optional[str] = None,
        error_code: typing.Optional[int] = None
    ):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.reason = reason
        self.error_code = error_code


def get_asset_info(asset_id: str) -> typing.Any:
    query = admin.query('GetAssetInfo', asset_id=asset_id)
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)
    
    response = net.send_query(query)
    if response.HasField('error_response'):
        err = response.error_response
        return IrohaException(
            err.message,
            reason=err.reason or None,
            error_code=err.error_code or None,
        )
    return response.asset_response.asset
