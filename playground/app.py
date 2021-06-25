import strawberry

from playground.schema import Mutation, Query

schema = strawberry.Schema(query=Query, mutation=Mutation)
