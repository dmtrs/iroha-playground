import enum

import strawberry

URI = strawberry.ID


@strawberry.enum
class TransactionStatus(enum.Enum):
    NONE = None
    COMMITTED = "COMMITTED"
    ENOUGH_SIGNATURES_COLLECTED = "ENOUGH_SIGNATURES_COLLECTED"
    REJECTED = "REJECTED"
    STATEFUL_VALIDATION_FAILED = "STATEFUL_VALIDATION_FAILED"
    STATELESS_VALIDATION_FAILED = "STATELESS_VALIDATION_FAILED"


@strawberry.input
class IDomain:
    uri: URI


@strawberry.input
class IAsset:
    id: str
    domain: IDomain
    precision: int


@strawberry.type
class Domain:
    uri: URI


@strawberry.type
class Asset:
    uri: URI
    precision: int

    @strawberry.field
    def id(self) -> str:
        id, *_ = self.uri.split("#")
        return id

    @strawberry.field
    def domain(self) -> Domain:
        *_, domain_id = self.uri.split("#")
        return Domain(uri=URI(domain_id))


@strawberry.type
class Account:
    uri: URI

    @strawberry.field
    def id(self) -> str:
        id, *_ = self.uri.split("@")
        return id

    @strawberry.field
    def domain(self) -> Domain:
        *_, domain_id = self.uri.split("@")
        return Domain(uri=URI(domain_id))


class AccountResolver:
    def __call__(self, *, uri: str) -> Account:
        return Account(uri=URI(uri))


@strawberry.type
class Transaction:
    uri: URI
    status: TransactionStatus
    commands: str

    creator_account_uri: strawberry.Private[URI]

    @strawberry.field
    def creator(self) -> Account:
        return AccountResolver()(uri=self.creator_account_uri)
