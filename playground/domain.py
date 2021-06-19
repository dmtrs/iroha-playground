import enum
import typing
import strawberry

@strawberry.enum
class TransactionStatus(enum.Enum):
    NONE = None
    COMMITTED = 'COMMITTED'
    ENOUGH_SIGNATURES_COLLECTED = 'ENOUGH_SIGNATURES_COLLECTED'
    REJECTED = 'REJECTED'
    STATEFUL_VALIDATION_FAILED = 'STATEFUL_VALIDATION_FAILED'

@strawberry.input
class IDomain:
    id: strawberry.ID

@strawberry.input
class IAsset:
    name: str
    domain: IDomain
    precision: int

@strawberry.type
class Domain:
    id: strawberry.ID

class DomainResolver:
    def __call__(self, id: strawberry.ID) -> Domain:
        return Domain(id=id)

@strawberry.type
class Asset:
    id: strawberry.ID
    precision: int

    domain_id: strawberry.Private[str]
    @strawberry.field
    def domain(self) -> Domain:
        return DomainResolver()(id=strawberry.ID(self.domain_id))

@strawberry.type
class Account:
    id: strawberry.ID

class AccountResolver:
    def __call__(self, *, id: strawberry.ID) -> Account:
        return Account(id=id)

@strawberry.type
class Transaction:
    hex_hash: strawberry.ID
    status: TransactionStatus
    commands: str

    creator_account_id: strawberry.Private[str]

    @strawberry.field
    def creator(self) -> Account:
        return AccountResolver()(id=strawberry.ID(self.creator_account_id))
