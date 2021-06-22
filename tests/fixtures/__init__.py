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
    from playground.iroha import (
        IrohaClient,
        IrohaGrpc,
    )
    mock_container = Container()

    MockIrohaGrpc = create_autospec(IrohaGrpc)

    mock_iroha_grpc = MockIrohaGrpc()
    # due to mock interferring the container __init__ signature read from punq
    # we set an explicit instance
    mock_container.register(
        IrohaGrpc,
        MockIrohaGrpc,
        instance=mock_iroha_grpc,
    )
    
    MockIrohaClient = create_autospec(IrohaClient)

    mock_iroha_client = MockIrohaClient(net=mock_iroha_grpc)
    # due to mock interferring the container __init__ signature read from punq
    # we set an explicit instance
    mock_container.register(
        IrohaClient, 
        MockIrohaClient,
        instance=mock_iroha_client,
    )

    import playground
    with patch.object(playground, 'container', mock_container):
        yield mock_container
