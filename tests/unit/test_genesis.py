import json
from dataclasses import asdict

from playground.genesis import (
    Query,
    GenesisBlock,
)

class TestGenesis:
    def test_ok(self, genesis_block: str ) -> None:
        actual: GenesisBlock = Query().default_genesis()
        assert json.dumps(asdict(actual))  == genesis_block
