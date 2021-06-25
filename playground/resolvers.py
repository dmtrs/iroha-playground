import typing

from playground import container
from playground.domain import URI, Asset, Transaction, TransactionStatus
from playground.iroha import IrohaClient, IrohaException


class ResolverException(Exception):
    pass


class AssetResolver:
    def __call__(self, uri: str) -> typing.Union[Asset, ResolverException]:
        try:
            _uri, precision = container.resolve(IrohaClient).get_asset_info(
                asset_id=uri
            )
            return Asset(
                uri=URI(_uri),
                precision=precision,
            )
        except IrohaException as e:
            return ResolverException(e)


class TransactionResolver:
    def __call__(
        self, uri: str
    ) -> typing.Union[typing.Iterable[Transaction], ResolverException]:
        try:
            for _uri, status, creator_account_id, commands in container.resolve(
                IrohaClient
            ).get_transactions(tx_hashes=[uri]):
                yield Transaction(
                    uri=URI(_uri),
                    status=TransactionStatus(status),
                    creator_account_uri=creator_account_id,
                    commands=commands,
                )
        except IrohaException as e:
            yield ResolverException(e)
