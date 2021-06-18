import strawberry

from playground.schema import (
    Query,
    Mutation,
)

schema = strawberry.Schema(query=Query, mutation=Mutation)
