import typing
import strawberry

from playground.iroha import (
    instance,
    IrohaClient,
    IrohaException,
)
from playground.domain import (
    Asset,
    Transaction,
    TransactionStatus,
)

class AssetResolver:
    _iroha: IrohaClient
    def __new__(cls, *, iroha: typing.Callable[[], IrohaClient]=instance) -> typing.Any:
        assert iroha
        if not hasattr(cls,'_inst'):
            cls._inst = super(AssetResolver, cls).__new__(cls)
            cls._inst._iroha = iroha()
        return cls._inst

    def __call__(self, asset_id: strawberry.ID) -> Asset:
        r = self._iroha.get_asset_info(asset_id=asset_id)
        if isinstance(r, IrohaException):
            raise r

        return Asset(
            asset_id=r.asset_id,
            domain_id=r.domain_id,
            precision=r.precision
        )

class TransactionResolver:
    _iroha: IrohaClient
    def __new__(cls, *, iroha: typing.Callable[[], IrohaClient]=instance) -> typing.Any:
        assert iroha
        if not hasattr(cls,'_inst'):
            cls._inst = super(TransactionResolver, cls).__new__(cls)
            cls._inst._iroha = iroha()
        return cls._inst

    def __call__(self, tx_hash: str) -> typing.Iterable[Transaction]:
        for r, status, creator_account_id in self._iroha.get_transactions(tx_hashes=[tx_hash]):
            yield Transaction(
                hex_hash=strawberry.ID(tx_hash),
                status=TransactionStatus(status),
                creator_account_id=creator_account_id,
            )
