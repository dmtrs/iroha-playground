import enum
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
            cls._inst._iroha = iroha
        return cls._inst

    def __call__(self, asset_id: strawberry.ID) -> Asset:
        r = self._iroha.get_asset_info(asset_id=asset_id)
        if isinstance(r, self._iroha.IrohaException):
            raise r

        return Asset(
            asset_id=r.asset_id,
            domain_id=r.domain_id,
            precision=r.precision
        )

@strawberry.enum
class TransactionStatus(enum.Enum):
    COMMITTED = 'COMMITTED'
    ENOUGH_SIGNATURES_COLLECTED = 'ENOUGH_SIGNATURES_COLLECTED'
    REJECTED = 'REJECTED'
    STATEFUL_VALIDATION_FAILED = 'STATEFUL_VALIDATION_FAILED'

@strawberry.type
class Transaction:
    hex_hash: strawberry.ID
    creator_account_id: str

    @strawberry.field
    def status(self) -> TransactionStatus:
        try:
            return self._status
        except AttributeError:
            self._status = TransactionStatus(TransactionResolver().status(self.hex_hash))

        return self._status

    def update_status(self, status: TransactionStatus) -> None:
        self._status = status

class TransactionResolver:
    def __new__(cls, *, iroha: typing.Any = iroha) -> typing.Any:
        assert iroha
        if not hasattr(cls,'_inst'):
            cls._inst = super(TransactionResolver, cls).__new__(cls)
            cls._inst._iroha = iroha
        return cls._inst

    def __call__(self, tx_hash: str) -> typing.Iterable[Transaction]: 
        for r, creator_account_id in self._iroha.get_transactions(tx_hashes=[tx_hash]):
            yield Transaction(hex_hash=tx_hash, creator_account_id=creator_account_id)

    def status(self, hex_hash: str) -> int:
        for r in self._iroha.tx_status(hex_hash=hex_hash):
            return r
        
        


@strawberry.type
class Query:
    asset: Asset = strawberry.field(resolver=AssetResolver().__call__)
    transaction: typing.List[Transaction] = strawberry.field(resolver=TransactionResolver().__call__)


@strawberry.input
class IAsset:
    asset_name: str
    domain_id: str
    precision: int

class AssetMutator:
    def __new__(cls, *, iroha: typing.Any = iroha) -> typing.Any:
        assert iroha
        if not hasattr(cls,'_inst'):
            cls._inst = super(AssetMutator, cls).__new__(cls)
            cls._inst._iroha = iroha
        return cls._inst

    def create_asset(self, input_asset: IAsset) -> Transaction:
        tx, status, creator_account_id = self._iroha.create_asset(
            asset_name=input_asset.asset_name,
            domain_id=input_asset.domain_id,
            precision=input_asset.precision,
        )
        if isinstance(tx, self._iroha.IrohaException):
            raise tx

        tx = Transaction(
            hex_hash=tx.decode('utf-8'),
            creator_account_id=creator_account_id,
        )
        tx.update_status(status)
        return tx

@strawberry.type
class Mutation:
    create_asset: Transaction = strawberry.mutation(AssetMutator().create_asset)

schema = strawberry.Schema(query=Query, mutation=Mutation)
