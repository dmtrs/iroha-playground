import punq

from playground.iroha import IrohaClient

container = punq.Container()
container.register(IrohaClient)
