from unittest.mock import Mock, create_autospec, patch

import pytest
import asyncio
from punq import Container


@pytest.fixture(scope="session")
def genesis_block() -> str:
    data = None
    with open("tests/fixtures/genesis_block.raw.json", "r") as genesis_block:
        data = genesis_block.read()
    return data


@pytest.fixture(scope="function", autouse=True)
def container(event_loop: asyncio.AbstractEventLoop) -> Container:
    from playground.concurrency import Runner
    from playground.iroha import IrohaAccount, IrohaClient, IrohaGrpc

    mock_container = Container()
    mock_container.register(asyncio.AbstractEventLoop, instance=event_loop)
    mock_container.register(Runner)

    mock_container.register(IrohaAccount, instance=IrohaAccount(
        id="admin@test",
        private_key="4148a3308e04975baa77ad2b5f4ac70f250506cf6cf388d3963ade2c68e5b2ad",
    ))

    MockIrohaGrpc = create_autospec(IrohaGrpc)
    # due to mock interferring the container __init__ signature read from punq
    # we set an explicit instance
    mock_container.register(
        IrohaGrpc,
        MockIrohaGrpc,
    )

    MockIrohaClient = create_autospec(IrohaClient)
    # due to mock interferring the container __init__ signature read from punq
    # we set an explicit instance
    mock_container.register(
        IrohaClient,
        instance=MockIrohaClient(
            account=mock_container.resolve(IrohaAccount),
            net=mock_container.resolve(IrohaGrpc),
            run=mock_container.resolve(Runner),
        ),
    )

    import playground

    with patch.object(playground, "container", mock_container):
        yield mock_container
