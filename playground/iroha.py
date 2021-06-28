import binascii
from typing import (
    Any,
    Coroutine,
    Optional,
    Tuple,
    List,
    Iterable,
)
import os

from playground.concurrency import run_in_threadpool

from iroha import Iroha as Iroha
from iroha import IrohaCrypto as IrohaCrypto
from iroha import IrohaGrpc as IrohaGrpc

ADMIN_ACCOUNT_ID = os.getenv("ADMIN_ACCOUNT_ID", "admin@test")
ADMIN_PRIVATE_KEY = os.getenv(
    "ADMIN_PRIVATE_KEY",
    "4148a3308e04975baa77ad2b5f4ac70f250506cf6cf388d3963ade2c68e5b2ad",
)


def init_client(account_id: str) -> Iroha:
    return Iroha(account_id)


admin = init_client(ADMIN_ACCOUNT_ID)


class IrohaException(Exception):
    def __init__(
        self,
        message: str,
        *,
        reason: Optional[str] = None,
        error_code: Optional[int] = None
    ):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.reason = reason
        self.error_code = error_code


class IrohaClient:
    _net: IrohaGrpc

    def __init__(self, net: IrohaGrpc):
        self._net = net

    def create_asset(self, *, asset_name:  str, domain_id: str, precision: int) -> Tuple[str, str, str, str]:
        tx = admin.transaction([
            admin.command('CreateAsset',
                asset_name=asset_name, 
                domain_id=domain_id,
                precision=precision,
            )
        ])
        IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)

        hex_hash = binascii.hexlify(IrohaCrypto.hash(tx))
        self._net.send_tx(tx)
        for s in self._net.tx_status_stream(tx, timeout=1):
            (status, *_) = s
            continue
        return (
            hex_hash.decode("utf-8"),
            str(status),
            str(tx.payload.reduced_payload.creator_account_id),
            str(tx.payload.reduced_payload.commands),
        )


    def get_transactions(self, *, tx_hashes: List[str], status: bool=True) -> Iterable[Tuple[str,str,str,str]]:
        response = self._send_query('GetTransactions', tx_hashes=[ bytes(tx, 'utf-8') for tx in tx_hashes ])

        for tx in response.transactions_response.transactions:
            (status, *_) = self._net.tx_status(tx)  # should async
            hex_hash = binascii.hexlify(IrohaCrypto.hash(tx))
            yield (
                hex_hash.decode("utf-8"),
                str(status),
                tx.payload.reduced_payload.creator_account_id,
                str(tx.payload.reduced_payload.commands),
            )

<<<<<<< Updated upstream
    def get_asset_info(self, *, asset_id: str) -> typing.Tuple[str, int]:
        response = self._send_query("GetAssetInfo", asset_id=asset_id)
        return (
            str(response.asset_response.asset_id),
            int(response.asset_response.precision),
        )

    def get_block(self, *, height: int = 1) -> typing.Any:
=======
    async def get_asset_info(self, *, asset_id: str) -> Tuple[str, int]:
        def _get_asset_info(*, asset_id: str) -> Tuple[str, int]:
            response = self._send_query('GetAssetInfo', asset_id=asset_id)
            return (
                str(response.asset_response.asset_id),
                int(response.asset_response.precision),
            )
        return await run_in_threadpool(_get_asset_info, asset_id=asset_id)

    def get_block(self, *, height: int=1) -> Any:
        assert height > 0
        response = self._send_query("GetBlock", height=height)
        return response

    def _send_query(self, name: str , **kwargs: Any) -> Any: 
        query = admin.query(name, **kwargs)
        IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)

        response = self._net.send_query(query)
        if response.HasField("error_response"):
            err = response.error_response
            raise IrohaException(
                err.message,
                reason=err.reason or None,
                error_code=err.error_code or None,
            )
        return response
