import typing
import enum
import strawberry
import dataclasses

@strawberry.enum
class DefaultAdminPermissions(enum.Enum):
    can_add_peer="can_add_peer"
    can_add_signatory="can_add_signatory"
    can_create_account="can_create_account"
    can_create_domain="can_create_domain"
    can_get_all_acc_ast="can_get_all_acc_ast"
    can_get_all_acc_ast_txs="can_get_all_acc_ast_txs"
    can_get_all_acc_detail="can_get_all_acc_detail"
    can_get_all_acc_txs="can_get_all_acc_txs"
    can_get_all_accounts="can_get_all_accounts"
    can_get_all_signatories="can_get_all_signatories"
    can_get_all_txs="can_get_all_txs"
    can_get_blocks="can_get_blocks"
    can_get_roles="can_get_roles"
    can_read_assets="can_read_assets"
    can_remove_signatory="can_remove_signatory"
    can_set_quorum="can_set_quorum"

@strawberry.enum
class DefaultUserPermissions(enum.Enum):
    can_add_signatory="can_add_signatory"
    can_get_my_acc_ast="can_get_my_acc_ast"
    can_get_my_acc_ast_txs="can_get_my_acc_ast_txs"
    can_get_my_acc_detail="can_get_my_acc_detail"
    can_get_my_acc_txs="can_get_my_acc_txs"
    can_get_my_account="can_get_my_account"
    can_get_my_signatories="can_get_my_signatories"
    can_get_my_txs="can_get_my_txs"
    can_grant_add_my_signatory="can_grant_can_add_my_signatory"
    can_grant_can_remove_my_signatory="can_grant_can_remove_my_signatory"
    can_grant_can_set_my_account_detail="can_grant_can_set_my_account_detail"
    can_grant_can_set_my_quorum="can_grant_can_set_my_quorum"
    can_grant_can_transfer_my_assets="can_grant_can_transfer_my_assets"
    can_receive="can_receive"
    can_remote_signatory="can_remove_signatory"
    can_set_quorum="can_set_quorum"
    can_transfer="can_transfer"

@strawberry.enum
class DefaultMoneyCreatorPermissions(enum.Enum):
    can_add_asset_qty="can_add_asset_qty"
    can_create_asset="can_create_asset"
    can_receive="can_receive"
    can_transfer="can_transfer"

@strawberry.type
class AddPeer:
    address: str
    peerKey: str

@strawberry.type
class AddPeerCommand:
    addPeer: AddPeer

@strawberry.type
class CreateRole:
    roleName: str
    permissions: typing.List[DefaultAdminPermissions]

@strawberry.type
class CreateRoleCommand:
    createRole: CreateRole

@strawberry.type
class ReducedPayload:
    commands: typing.List[typing.Union[
        AddPeerCommand,
        CreateRoleCommand,
    ]]
    quorum: int = 1

@strawberry.type
class TransactionPayload:
    reducedPayload: ReducedPayload

@strawberry.type
class Transaction:
    payload: TransactionPayload

@strawberry.type
class BlockPayload:
    transactions: typing.List[Transaction] = dataclasses.field(default_factory=list)
    txNumber: int = 0
    height: str = "0"
    prevBlockHash: str = ''

@strawberry.type
class Block:
    payload: BlockPayload

@strawberry.type
class GenesisBlock:
    _id: strawberry.ID
    block_v1: Block

@strawberry.type
class Query:
    @strawberry.field
    def default_genesis(self) -> GenesisBlock:
        commands: typing.List[typing.Union[AddPeerCommand, CreateRoleCommand]] = [
            AddPeerCommand(
                addPeer=AddPeer(
                    address='127.0.0.1:10001',
                    peerKey='bddd58404d1315e0eb27902c5d7c8eb0602c16238f005773df406bc191308929',
                )
            ),
            CreateRoleCommand(
                createRole=CreateRole(
                    roleName='admin',
                    permissions=[ p for p in DefaultAdminPermissions ]
                ),
            )
        ]
        raw_commands: typing.List[typing.Dict[str, typing.Dict[str, typing.Any]]] = [
            {
                'addPeer': {
                    'peer': {
                        'address':'127.0.0.1:10001',
                        'peerKey': 'bddd58404d1315e0eb27902c5d7c8eb0602c16238f005773df406bc191308929'
                    },
                },
            },
            {
                'createRole': {
                    'roleName': 'admin',
                    'permissions': [ p.value for p in DefaultAdminPermissions ]
                },
            },
            {
                'createRole': {
                    'roleName': 'user',
                    'permissions': [ p.value for p in DefaultUserPermissions ]
                },
            },
            {
                'createRole': {
                    'roleName': 'money_creator',
                    'permissions': [ p.value for p in DefaultMoneyCreatorPermissions ],
                },
            },
            {
                'createDomain': {
                    'domainId': 'test',
                    'defaultRole': 'user',
                },
            },
            {
                'createAsset': {
                    'assetName': 'coin',
                    'domainId': 'test',
                    'precision': 2,
                },
            },
            {
                'createAccount': {
                    'accountName': 'admin',
                    'domainId': 'test',
                    'publicKey': '313a07e6384776ed95447710d15e59148473ccfc052a681317a72a69f2a49910',
                },
            },
            {
                'createAccount': {
                    'accountName': 'test',
                    'domainId': 'test',
                    'publicKey': '716fe505f69f18511a1b083915aa9ff73ef36e6688199f3959750db38b8f4bfc',
                },
            },
            { 'appendRole': { 'accountId': 'admin@test', 'roleName': 'admin' } },
            { 'appendRole': { 'accountId': 'admin@test', 'roleName': 'money_creator' } },
        ]
        import uuid
        return GenesisBlock(
            _id=strawberry.ID(str(uuid.uuid4())),
            block_v1=Block(
                payload=BlockPayload(
                    transactions=[
                        Transaction(
                            payload=TransactionPayload(
                                reducedPayload=ReducedPayload(
                                    commands=commands,
                                    quorum=1,
                                )
                            )
                        ),
                    ],
                    txNumber=1,
                    height="1",
                    prevBlockHash='0000000000000000000000000000000000000000000000000000000000000000',
                )
            )
        )

schema = strawberry.Schema(query=Query)
