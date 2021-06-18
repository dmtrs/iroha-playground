import typing
import strawberry

from playground import container
from playground.iroha import (
    IrohaClient,
    IrohaException,
)
from playground.domain import (
    Asset,
    Transaction,
    TransactionStatus,
)

class AssetResolver:
    def __call__(self, asset_id: strawberry.ID) -> Asset:
        r = container.resolve(IrohaClient).get_asset_info(asset_id=asset_id)
        if isinstance(r, IrohaException):
            raise r

        return Asset(
            asset_id=r.asset_id,
            domain_id=r.domain_id,
            precision=r.precision
        )

class TransactionResolver:
    def __call__(self, tx_hash: str) -> typing.Iterable[Transaction]:
        for r, status, creator_account_id in container.resolve(IrohaClient).get_transactions(tx_hashes=[tx_hash]):
            yield Transaction(
                hex_hash=strawberry.ID(tx_hash),
                status=TransactionStatus(status),
                creator_account_id=creator_account_id,
            )
