import typing
from punq import Container

from playground.iroha import(
    IrohaClient,
    IrohaException,
)


class TestApp:
    def test_ok(self, container: Container) -> None:
        from playground.app import schema

        container.resolve(IrohaClient).get_asset_info.return_value = ('coin#test', 0,)

        query = '''
        query asset {
          asset(uri:"coin#test") {
              uri
              id
              domain {
                id
              }
              precision
          }
        }
        '''

        expected = {
            'asset': {
                'uri': 'coin#test',
                'id': 'coin',
                'domain': {
                    'id': 'test'
                },
                'precision': 0,
            }
        }
        result = schema.execute_sync(query)

        assert not result.errors
        assert result.data == expected

    def test_exception(self, container: Container) -> None:
        from playground.app import schema

        container.resolve(IrohaClient).get_asset_info.side_effect = IrohaException(message='mock')

        query = '''
        query asset {
          asset(uri:"foo") {
              uri
          }
        }
        '''

        result = schema.execute_sync(query)

        assert result.errors








