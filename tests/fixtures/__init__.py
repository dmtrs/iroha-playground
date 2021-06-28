from unittest.mock import Mock, create_autospec, patch

import pytest
from punq import Container


@pytest.fixture(scope="session")
def genesis_block() -> str:
    data = None
    with open("tests/fixtures/genesis_block.raw.json", "r") as genesis_block:
        data = genesis_block.read()
    return data


@pytest.fixture(scope="session", autouse=True)
def container() -> Container:
    from playground.iroha import IrohaAccount, IrohaClient, IrohaGrpc

    mock_container = Container()

    mock_account = IrohaAccount(
        id="admin@test",
        private_key="4148a3308e04975baa77ad2b5f4ac70f250506cf6cf388d3963ade2c68e5b2ad",
    )

    mock_container.register(IrohaAccount, instance=mock_account)

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

    mock_iroha_client = MockIrohaClient(account=mock_account, net=mock_iroha_grpc)
    # due to mock interferring the container __init__ signature read from punq
    # we set an explicit instance
    mock_container.register(
        IrohaClient,
        MockIrohaClient,
        instance=mock_iroha_client,
    )

    import playground

    with patch.object(playground, "container", mock_container):
        yield mock_container
