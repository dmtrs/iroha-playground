import enum
import typing
import strawberry

from playground.domain import (
    IAsset,
    Asset,
    Transaction,
)
from playground.resolvers import (
    AssetResolver,
    TransactionResolver,
)
from playground.mutators import (
    AssetMutator
)


@strawberry.type
class Query:
    asset: Asset = strawberry.field(resolver=AssetResolver().__call__)
    transaction: typing.List[Transaction] = strawberry.field(resolver=TransactionResolver().__call__)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_asset(self, *, input_asset: IAsset) -> Transaction: 
        return AssetMutator().__call__(input_asset=input_asset)

schema = strawberry.Schema(query=Query, mutation=Mutation)
