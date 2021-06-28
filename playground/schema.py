import typing

import strawberry

from playground.domain import Asset, IAsset, Transaction
from playground.mutators import AssetMutator
from playground.resolvers import AssetResolver, TransactionResolver


@strawberry.type
class Query:
    @strawberry.field
    async def asset(self, *, uri: str) -> Asset:
        return await AssetResolver()(uri=uri)

    transaction: typing.List[Transaction] = strawberry.field(
        resolver=TransactionResolver().__call__
    )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_asset(self, *, input_asset: IAsset) -> Transaction:
        return AssetMutator().__call__(input_asset=input_asset)


schema = strawberry.Schema(query=Query, mutation=Mutation)
