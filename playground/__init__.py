import os

import punq

from playground.iroha import IrohaAccount, IrohaClient, IrohaGrpc

container = punq.Container()

IROHA_HOST_ADDR = os.getenv("IROHA_HOST_ADDR", "node")
IROHA_PORT = os.getenv("IROHA_PORT", "50051")

ADMIN_ACCOUNT_ID = os.getenv("ADMIN_ACCOUNT_ID", "admin@test")
ADMIN_PRIVATE_KEY = os.getenv(
    "ADMIN_PRIVATE_KEY",
    "4148a3308e04975baa77ad2b5f4ac70f250506cf6cf388d3963ade2c68e5b2ad",
)

container.register(
    IrohaGrpc, instance=IrohaGrpc("{}:{}".format(IROHA_HOST_ADDR, IROHA_PORT))
)

container.register(
    IrohaAccount,
    instance=IrohaAccount(
        id=ADMIN_ACCOUNT_ID,
        private_key=ADMIN_PRIVATE_KEY,
    ),
)
container.register(IrohaClient)
