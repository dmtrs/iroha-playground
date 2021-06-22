import os
import punq

from playground.iroha import (
    IrohaClient,
    IrohaGrpc,
)

container = punq.Container()

IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', 'node')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
container.register(IrohaGrpc, instance=IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR, IROHA_PORT)))

container.register(IrohaClient)
