import pytest

@pytest.fixture(scope="session")
def genesis_block() -> str:
    data=None
    with open('tests/fixtures/genesis_block.raw.json', 'r') as genesis_block:
        data=genesis_block.read()
    return data
