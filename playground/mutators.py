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
    URI,
)


class MutatorException(Exception):
    pass


class AssetMutator:
    def __call__(self, *, input_asset: IAsset) -> Transaction:
        try:
            tx, status, creator_account_id, commands = container.resolve(IrohaClient).create_asset(
                asset_name=input_asset.id,
                domain_id=input_asset.domain.id,
                precision=input_asset.precision,
            )
        except IrohaException as e:
            raise MutatorException(e)

        return Transaction(
            uri=strawberry.ID(tx),
            creator_account_uri=creator_account_id,
            status=TransactionStatus(status),
            commands=commands,
        )

