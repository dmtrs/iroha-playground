import typing

import strawberry

from playground.iroha import (
    instance,
    IrohaClient,
    IrohaException,
)
from playground.domain import (
    IAsset,
    Transaction,
    TransactionStatus, 
)

class AssetMutator:
    _iroha: IrohaClient
    def __new__(cls, *, iroha: typing.Callable[[], IrohaClient]=instance) -> typing.Any:
        assert iroha
        if not hasattr(cls,'_inst'):
            cls._inst = super(AssetMutator, cls).__new__(cls)
            cls._inst._iroha = iroha()
        return cls._inst

    def __call__(self, *, input_asset: IAsset) -> Transaction:
        tx, status, creator_account_id = self._iroha.create_asset(
            asset_name=input_asset.asset_name,
            domain_id=input_asset.domain_id,
            precision=input_asset.precision,
        )
        if isinstance(tx, IrohaException):
            raise tx

        return Transaction(
            hex_hash=strawberry.ID(tx.decode('utf-8')),
            creator_account_id=creator_account_id,
            status=TransactionStatus(status),
        )

