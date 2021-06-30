from punq import Container

from playground.domain import URI, Asset, Transaction, TransactionStatus
from playground.iroha import IrohaClient, IrohaException


class TestApp:
    def test_mutation_create_asset(self, container: Container) -> None:
        from playground.app import schema

        container.resolve(IrohaClient).create_asset.return_value = Transaction(
            uri=URI("tx_hex_hash"),
            status=TransactionStatus("COMMITTED"),
            creator_account_uri=URI("admin@test"),
            commands="commands",
        )

        mutation = """
        mutation createAsset($inputAsset:IAsset!) {
          createAsset(inputAsset:$inputAsset) {
            uri
          }
        }
        """
        variables = {
            "inputAsset": {
                "id": "newcoin",
                "domain": {
                    "uri": "foo",
                },
                "precision": 0,
            }
        }
        result = schema.execute_sync(mutation, variable_values=variables)

        expected = {
            "createAsset": {
                "uri": "tx_hex_hash",
            }
        }

        assert not result.errors
        assert result.data == expected

    def test_mutation_create_asset_exception(self, container: Container) -> None:
        from playground.app import schema

        container.resolve(IrohaClient).create_asset.side_effect = IrohaException(
            message="mock"
        )

        mutation = """
        mutation createAsset($inputAsset:IAsset!) {
          createAsset(inputAsset:$inputAsset) {
            uri
          }
        }
        """
        variables = {
            "inputAsset": {
                "id": "newcoin",
                "domain": {
                    "id": "foo",
                },
                "precision": 0,
            }
        }
        result = schema.execute_sync(mutation, variable_values=variables)

        assert result.errors

    def test_query_asset_ok(self, container: Container) -> None:
        from playground.app import schema

        container.resolve(IrohaClient).get_asset.return_value = Asset(
            uri=URI("coin#test"),
            precision=0,
        )

        query = """
        query asset {
          asset(uri:"coin#test") {
              uri
              id
              domain {
                uri
              }
              precision
          }
        }
        """

        expected = {
            "asset": {
                "uri": "coin#test",
                "id": "coin",
                "domain": {"uri": "test"},
                "precision": 0,
            }
        }
        result = schema.execute_sync(query)

        assert not result.errors
        assert result.data == expected

    def test_query_asset_exception(self, container: Container) -> None:
        from playground.app import schema

        container.resolve(IrohaClient).get_asset.side_effect = IrohaException(
            message="mock"
        )

        query = """
        query asset {
          asset(uri:"foo") {
              uri
          }
        }
        """

        result = schema.execute_sync(query)

        assert result.errors

    def test_query_asset(self, container: Container) -> None:
        from playground.app import schema

        container.resolve(IrohaClient).get_transactions.return_value = [ Transaction(
            uri=URI("foo"),
            status=TransactionStatus("REJECTED"),
            creator_account_uri=URI("bar@test"),
            commands="commands",
        ) ]

        query = """
        query transactions {
            transaction(uris: [ "foo" ]) {
                uri
                creator {
                    uri
                    domain {
                        uri
                    }
                    id
                }
                commands
            }
        }
        """

        expected = {
            "transaction": [
                {
                    "uri": "foo",
                    "creator": {
                        "uri": "bar@test",
                        "domain": {
                            "uri": "test",
                        },
                        "id": "bar",
                    },
                    "commands": "commands",
                }
            ]
        }

        result = schema.execute_sync(query)

        assert not result.errors
        assert result.data == expected

    def test_query_transaction_exception(self, container: Container) -> None:
        from playground.app import schema

        container.resolve(IrohaClient).get_transactions.side_effect = IrohaException(
            message="mock"
        )

        query = """
        query transactions {
            transaction(uri:"foo") {
                uri
            }
        }
        """

        result = schema.execute_sync(query)

        assert result.errors
