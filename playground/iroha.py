import binascii
from dataclasses import dataclass
from typing import (
    Any,
    Iterable,
    List,
    Optional,
    Tuple,
)
from collections.abc import (
    Awaitable
)


from playground.concurrency import Runner

from iroha import Iroha as Iroha
from iroha import IrohaCrypto as IrohaCrypto
from iroha import IrohaGrpc as IrohaGrpc


@dataclass
class IrohaAccount:
    id: str
    private_key: str

    @property
    def client(self) -> Iroha:
        return Iroha(self.id)


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
    _account: IrohaAccount
    _run: Runner

    def __init__(self, *, account: IrohaAccount, net: IrohaGrpc, run: Runner):
        self._net = net
        self._account = account
        self._run = run

    def create_asset(
        self, *, asset_name: str, domain_id: str, precision: int
    ) -> Tuple[str, str, str, str]:
        tx = self._account.client.transaction(
            [
                self._account.client.command(
                    "CreateAsset",
                    asset_name=asset_name,
                    domain_id=domain_id,
                    precision=precision,
                )
            ]
        )
        IrohaCrypto.sign_transaction(tx, self._account.private_key)

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

    def get_transactions(
        self, *, tx_hashes: List[str], status: bool = True
    ) -> Iterable[Tuple[str, str, str, str]]:
        response = self._send_query(
            "GetTransactions", tx_hashes=[bytes(tx, "utf-8") for tx in tx_hashes]
        )

        for tx in response.transactions_response.transactions:
            (status, *_) = self._net.tx_status(tx)  # should async
            hex_hash = binascii.hexlify(IrohaCrypto.hash(tx))
            yield (
                hex_hash.decode("utf-8"),
                str(status),
                tx.payload.reduced_payload.creator_account_id,
                str(tx.payload.reduced_payload.commands),
            )

    def get_asset_info(self, *, asset_id: str) -> Awaitable[Tuple[str, int]]:
        def _get_asset_info(*, asset_id: str) -> Tuple[str, int]:
            response = self._send_query("GetAssetInfo", asset_id=asset_id)
            print(response)
            return (
                str(response.asset_response.asset.asset_id),
                int(response.asset_response.asset.precision),
            )

        return self._run(_get_asset_info, asset_id=asset_id)

    def get_block(self, *, height: int = 1) -> Any:
        assert height > 0
        response = self._send_query("GetBlock", height=height)
        return response

    def _send_query(self, name: str, **kwargs: Any) -> Any:
        query = self._account.client.query(name, **kwargs)
        IrohaCrypto.sign_query(query, self._account.private_key)

        response = self._net.send_query(query)
        if response.HasField("error_response"):
            err = response.error_response
            raise IrohaException(
                err.message,
                reason=err.reason or None,
                error_code=err.error_code or None,
            )
        return response
