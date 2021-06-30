import binascii
from dataclasses import dataclass
from typing import Any, Iterable, List, Optional

from iroha import Iroha as Iroha
from iroha import IrohaCrypto as IrohaCrypto
from iroha import IrohaGrpc as IrohaGrpc
from playground.domain import URI, Asset, IAsset, Transaction, TransactionStatus


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

    def __init__(self, account: IrohaAccount, net: IrohaGrpc):
        self._net = net
        self._account = account

    def create_asset(self, *, input_asset: IAsset) -> Transaction:
        tx = self._account.client.transaction(
            [
                self._account.client.command(
                    "CreateAsset",
                    asset_name=input_asset.id,
                    domain_id=input_asset.domain.uri,
                    precision=input_asset.precision,
                )
            ]
        )
        IrohaCrypto.sign_transaction(tx, self._account.private_key)

        hex_hash = binascii.hexlify(IrohaCrypto.hash(tx))
        self._net.send_tx(tx)
        for s in self._net.tx_status_stream(tx, timeout=1):
            (status, *_) = s
            continue
        return Transaction(
            uri=URI(hex_hash.decode("utf-8")),
            status=TransactionStatus(str(status)),
            creator_account_uri=URI(str(tx.payload.reduced_payload.creator_account_id)),
            commands=str(tx.payload.reduced_payload.commands),
        )

    def get_transactions(self, *, uris: List[URI]) -> Iterable[Transaction]:
        response = self._send_query(
            "GetTransactions", tx_hashes=[bytes(uri, "utf-8") for uri in uris]
        )
        for tx in response.transactions_response.transactions:
            (status, *_) = self._net.tx_status(tx)  # should async
            hex_hash = binascii.hexlify(IrohaCrypto.hash(tx))
            yield Transaction(
                uri=URI(hex_hash.decode("utf-8")),
                status=TransactionStatus(str(status)),
                creator_account_uri=URI(
                    str(tx.payload.reduced_payload.creator_account_id)
                ),
                commands=str(tx.payload.reduced_payload.commands),
            )

    def get_asset(self, *, uri: URI) -> Asset:
        response = self._send_query("GetAssetInfo", asset_id=uri)
        return Asset(
            uri=URI(str(response.asset_response.asset_id)),
            precision=int(response.asset_response.precision),
        )

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
