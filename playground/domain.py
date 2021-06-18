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
class IAsset:
    asset_name: str
    domain_id: str
    precision: int

@strawberry.type
class Asset:
    asset_id: strawberry.ID
    domain_id: str
    precision: int

@strawberry.type
class Transaction:
    hex_hash: strawberry.ID
    creator_account_id: str
    status: TransactionStatus
