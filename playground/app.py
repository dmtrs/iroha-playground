import strawberry
import playground.iroha as iroha


@strawberry.type
class Asset:
    asset_id: strawberry.ID
    domain_id: str
    precision: int

    def __new__(cls, *args, **kwargs):
        f = super(Asset, cls).__new__(cls)
        f.asset_id = kwargs['asset_id']
        f.domain_id = kwargs['asset_id']
        f.precision = kwargs['precision']
        return f


@strawberry.type
class Query:
    @strawberry.field
    def get_asset(asset_id: strawberry.ID) -> Asset:
        r = iroha.get_asset_info(asset_id)
        return Asset(
            asset_id=r.asset_id,
            domain_id=r.domain_id,
            precision=r.precision,
        )

schema = strawberry.Schema(query=Query)
