from unittest.mock import ANY, Mock

from punq import Container

from playground.domain import (
    URI,
    Asset,
    IAsset,
    IDomain,
    Transaction,
    TransactionStatus,
)
from playground.iroha import IrohaAccount, IrohaClient, IrohaCrypto, IrohaGrpc


class TestIrohaClient:
    def test_get_asset(self, container: Container) -> None:
        mock_net = container.resolve(IrohaGrpc)
        mock_net.send_query.return_value = Mock(
            HasField=lambda *_: False,
            asset_response=Mock(
                asset_id="foo#bar",
                precision=1,
            ),
        )

        account = container.resolve(IrohaAccount)
        client = IrohaClient(account=account, net=mock_net)

        assert Asset(uri=URI("foo#bar"), precision=1) == client.get_asset(
            uri=URI("foo#bar"),
        )

    def test_create_asset_ok(self, container: Container) -> None:
        mock_net = container.resolve(IrohaGrpc)
        mock_net.send_tx.return_value = None
        mock_net.tx_status_stream.return_value = [("COMMITTED",)]

        account = container.resolve(IrohaAccount)
        client = IrohaClient(account=account, net=mock_net)

        actual = client.create_asset(
            input_asset=IAsset(
                id="foo",
                domain=IDomain(uri=URI("bar")),
                precision=1,
            )
        )
        expected = Transaction(
            uri=ANY,
            status=TransactionStatus("COMMITTED"),
            creator_account_uri=URI(container.resolve(IrohaAccount).id),
            commands=ANY,
        )
        assert expected == actual

        assert len(actual.uri) == 64
        assert (
            actual.commands.replace("\n", "")
            == '[create_asset {  asset_name: "foo"  domain_id: "bar"  precision: 1}]'
        )

    def test_get_transactions_ok(self, container: Container) -> None:
        mock_net = container.resolve(IrohaGrpc)
        mock_net.send_query.return_value = Mock(
            HasField=lambda *_: False,
            transactions_response=Mock(
                transactions=[
                    Mock(
                        payload=Mock(
                            reduced_payload=Mock(
                                creator_account_id="bar@test",
                                commands="*",
                            )
                        )
                    )
                ],
            ),
        )
        mock_net.tx_status.return_value = ["COMMITTED"]

        account = container.resolve(IrohaAccount)
        client = IrohaClient(account=account, net=mock_net)

        client._Crypto = Mock(IrohaCrypto)
        client._Crypto.hash.return_value = b"expected_uri"

        actual = client.get_transactions(uris=[URI("foo")])

        expected = [
            Transaction(
                uri=URI("65787065637465645f757269"),
                status=TransactionStatus("COMMITTED"),
                creator_account_uri=URI(
                    "bar@test"
                ),  # container.resolve(IrohaAccount).id),
                commands="*",
            )
        ]
        assert expected == list(actual)
