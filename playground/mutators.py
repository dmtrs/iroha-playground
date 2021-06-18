import typing

import strawberry

from playground import container
from playground.iroha import (
    IrohaClient,
    IrohaException,
)
from playground.domain import (
    IAsset,
    Transaction,
    TransactionStatus, 
)

class AssetMutator:
    def __call__(self, *, input_asset: IAsset) -> Transaction:
        tx, status, creator_account_id = container.resolve(IrohaClient).create_asset(
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

