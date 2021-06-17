import enum
import typing
import strawberry
# import playground.iroha as iroha

from playground.iroha import (IrohaClient, instance, IrohaException)

@strawberry.type
class Asset:
    asset_id: strawberry.ID
    domain_id: str
    precision: int

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

@strawberry.enum
class TransactionStatus(enum.Enum):
    NONE = None
    COMMITTED = 'COMMITTED'
    ENOUGH_SIGNATURES_COLLECTED = 'ENOUGH_SIGNATURES_COLLECTED'
    REJECTED = 'REJECTED'
    STATEFUL_VALIDATION_FAILED = 'STATEFUL_VALIDATION_FAILED'

@strawberry.type
class Transaction:
    hex_hash: strawberry.ID
    creator_account_id: str
    __status: typing.Optional[TransactionStatus] = None

    @strawberry.field
    def status(self) -> typing.Optional[TransactionStatus]:
        if not self.__status:
            self.___status = TransactionStatus(TransactionResolver().status(self.hex_hash))

        return self.__status

    def update_status(self, status: TransactionStatus) -> None:
        self._status = status

class TransactionResolver:
    _iroha: IrohaClient
    def __new__(cls, *, iroha: typing.Callable[[], IrohaClient]=instance) -> typing.Any:
        assert iroha
        if not hasattr(cls,'_inst'):
            cls._inst = super(TransactionResolver, cls).__new__(cls)
            cls._inst._iroha = iroha()
        return cls._inst

    def __call__(self, tx_hash: str) -> typing.Iterable[Transaction]: 
        for r, creator_account_id in self._iroha.get_transactions(tx_hashes=[tx_hash]):
            yield Transaction(hex_hash=strawberry.ID(tx_hash), creator_account_id=creator_account_id)

    def status(self, hex_hash: str) -> typing.Optional[str]:
        for r in self._iroha.tx_status(hex_hash=hex_hash):
            return str(r)
        return None
        
        


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
    _iroha: IrohaClient
    def __new__(cls, *, iroha: typing.Callable[[], IrohaClient]=instance) -> typing.Any:
        assert iroha
        if not hasattr(cls,'_inst'):
            cls._inst = super(AssetMutator, cls).__new__(cls)
            cls._inst._iroha = iroha
        return cls._inst

    def create_asset(self, *, input_asset: IAsset) -> Transaction:
        tx, status, creator_account_id = self._iroha.create_asset(
            asset_name=input_asset.asset_name,
            domain_id=input_asset.domain_id,
            precision=input_asset.precision,
        )
        if isinstance(tx, IrohaException):
            raise tx

        final_tx = Transaction(
            hex_hash=strawberry.ID(tx.decode('utf-8')),
            creator_account_id=creator_account_id,
        )
        final_tx.update_status(TransactionStatus(status))
        return final_tx

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_asset(self, input_asset: IAsset) -> Transaction:
        return AssetMutator().create_asset(input_asset=input_asset)

schema = strawberry.Schema(query=Query, mutation=Mutation)
