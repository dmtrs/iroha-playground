import asyncio
import pytest
from asyncmock import AsyncMock

from punq import Container

from playground.iroha import IrohaClient, IrohaException, IrohaAccount


class TestApp:
    @pytest.mark.asyncio
    async def test_mutation_create_asset(self, container: Container) -> None:
        from playground.app import schema

        container.resolve(IrohaClient).create_asset.return_value = (
            "tx_hex_hash",
            "COMMITTED",
            "admin@test",
            "commands",
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
        result = await schema.execute(mutation, variable_values=variables)

        expected = {
            "createAsset": {
                "uri": "tx_hex_hash",
            }
        }

        assert not result.errors
        assert result.data == expected

    @pytest.mark.asyncio
    async def test_mutation_create_asset_exception(self, container: Container) -> None:
        from playground.app import schema

        container.resolve(IrohaClient).create_asset = AsyncMock(side_effect = IrohaException(
            message="mock"
        ))

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
        result = await schema.execute(mutation, variable_values=variables)

        assert result.errors

    @pytest.mark.asyncio
    async def test_query_asset_ok(self, container: Container) -> None:
        from playground.app import schema
        container.resolve(IrohaClient).get_asset_info = AsyncMock(return_value=(
            "coin#test",
            0,
        ))

        query = """
        query asset {
          asset(uri:"coin#test") {
              uri
              id
              domain {
                id
              }
              precision
          }
        }
        """

        expected = {
            "asset": {
                "uri": "coin#test",
                "id": "coin",
                "domain": {"id": "test"},
                "precision": 0,
            }
        }
        result = await schema.execute(query)

        assert not result.errors
        assert result.data == expected

    @pytest.mark.asyncio
    async def test_query_asset_exception(self, container: Container) -> None:
        from playground.app import schema

        container.resolve(IrohaClient).get_asset_info.side_effect = IrohaException(
            message="mock"
        )

        query = """
        query asset {
          asset(uri:"foo") {
              uri
          }
        }
        """

        result = await schema.execute(query)

        assert result.errors

    @pytest.mark.asyncio
    async def test_query_asset(self, container: Container) -> None:
        from playground.app import schema

        container.resolve(IrohaClient).get_transactions.return_value = [
            (
                "foo",
                "REJECTED",
                "bar@test",
                "commands",
            ),
        ]

        query = """
        query transactions {
            transaction(uri:"foo") {
                uri
                creator {
                    uri
                    domain {
                        id
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
                            "id": "test",
                        },
                        "id": "bar",
                    },
                    "commands": "commands",
                }
            ]
        }

        result = await schema.execute(query)

        assert not result.errors
        assert result.data == expected

    @pytest.mark.asyncio
    async def test_query_transaction_exception(self, container: Container) -> None:
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

        result = await schema.execute(query)

        assert result.errors
