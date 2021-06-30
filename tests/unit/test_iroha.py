from unittest.mock import Mock

from punq import Container

from playground.domain import URI, Asset
from playground.iroha import IrohaAccount, IrohaClient, IrohaGrpc


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

        assert Asset(uri=URI('foo#bar'), precision=1) == client.get_asset(
            uri=URI("foo#bar"),
        )

    def test_create_asset_ok(self, container: Container) -> None:
        mock_net = container.resolve(IrohaGrpc)
        mock_net.send_tx.return_value = None
        mock_net.tx_status_stream.return_value = [("COMMITTED",)]

        account = container.resolve(IrohaAccount)
        client = IrohaClient(account=account, net=mock_net)

        (hex_hash, status, creator_account_id, commands,) = client.create_asset(
            asset_name="foo",
            domain_id="bar",
            precision=1,
        )
        assert len(hex_hash) == 64
        assert status == "COMMITTED"
        assert creator_account_id == container.resolve(IrohaAccount).id
        assert (
            commands.replace("\n", "")
            == '[create_asset {  asset_name: "foo"  domain_id: "bar"  precision: 1}]'
        )
