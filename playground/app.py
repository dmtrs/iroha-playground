import typing
import strawberry
import playground.iroha as iroha

@strawberry.type
class Asset:
    asset_id: strawberry.ID
    domain_id: str
    precision: int

class AssetResolver:
    def __new__(cls, *, iroha: typing.Any = iroha) -> typing.Any:
        assert iroha
        if not hasattr(cls,'_inst'):
            cls._inst = super(AssetResolver, cls).__new__(cls)
            cls._iroha = iroha
        return cls._inst

    def __call__(self, asset_id: strawberry.ID) -> Asset:
        r = iroha.get_asset_info(asset_id)
        if isinstance(r, iroha.IrohaException):
            raise r

        return Asset(
            asset_id=r.asset_id,
            domain_id=r.domain_id,
            precision=r.precision
        )

@strawberry.type
class Query:
    asset: Asset = strawberry.field(resolver=AssetResolver().__call__)

schema = strawberry.Schema(query=Query)
