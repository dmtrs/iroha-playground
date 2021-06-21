import typing
from punq import Container

from playground.iroha import IrohaClient


class TestOk:
    def test_ok(self, container: Container) -> None:
        from playground.app import schema

        container.resolve(IrohaClient).get_asset_info.return_value = ('coin#test', 0,)

        query = '''
        query asset {
          asset(uri:"coin#test") {
              uri
          }
        }
        '''

        expected = {
            'asset': {
                'uri': 'coin#test'
            }
        }
        result = schema.execute_sync(query)

        assert not result.errors
        assert result.data == expected




