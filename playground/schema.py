import typing

import strawberry

from playground import container
from playground.domain import URI, Asset, IAsset, Transaction
from playground.iroha import IrohaClient


@strawberry.type
class Query:
    @strawberry.field
    def asset(self, uri: URI = URI("foo#test")) -> Asset:
        client: IrohaClient = container.resolve(IrohaClient)
        return client.get_asset(uri=uri)

    @strawberry.field
    def transaction(self, uris: typing.List[URI]) -> typing.List[Transaction]:
        client: IrohaClient = container.resolve(IrohaClient)
        return list(client.get_transactions(uris=uris))


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_asset(self, *, input_asset: IAsset) -> Transaction:
        client: IrohaClient = container.resolve(IrohaClient)
        return client.create_asset(input_asset=input_asset)


schema = strawberry.Schema(query=Query, mutation=Mutation)
