import pytest

from unittest.mock import (
    create_autospec,
    Mock,
    patch,
)
from punq import Container

@pytest.fixture(scope="session")
def genesis_block() -> str:
    data=None
    with open('tests/fixtures/genesis_block.raw.json', 'r') as genesis_block:
        data=genesis_block.read()
    return data

@pytest.fixture(scope="session", autouse=True)
def container() -> Container:
    from playground.iroha import IrohaClient
    mock_container = Container()
    mock_container.register(IrohaClient, create_autospec(IrohaClient))

    import playground
    with patch.object(playground, 'container', mock_container):
        yield mock_container
