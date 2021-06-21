import typing
import strawberry

from playground import container
from playground.iroha import (
    IrohaClient,
    IrohaException,
)
from playground.domain import (
    Asset,
    Transaction,
    TransactionStatus,
    URI,
)

class ResolverException(Exception):
    pass
    
class AssetResolver:
    def __call__(self, uri: str) -> Asset:
        try:
            print(container.resolve(IrohaClient))
            _uri, precision = container.resolve(IrohaClient).get_asset_info(asset_id=uri) 
            return Asset(
                uri=URI(_uri),
                precision=precision,
            )
        except IrohaException as e:
            raise ResolverException(e)

class TransactionResolver:
    def __call__(self, uri: str) -> typing.Iterable[Transaction]:
        try:
            for _uri, status, creator_account_id, commands in container.resolve(IrohaClient).get_transactions(tx_hashes=[uri]):
                yield Transaction(
                    uri=URI(_uri),
                    status=TransactionStatus(status),
                    creator_account_uri=creator_account_id,
                    commands=commands,
                )
        except IrohaException as e:
            raise ResolverException(e)
