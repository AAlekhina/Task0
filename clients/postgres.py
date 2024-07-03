import psycopg2

class PostgresClient:
    def __init__(self, connection_string: str) -> None:
        self.connect = psycopg2.connect(connection_string)

    def execute(self, query: str, **kwargs) -> None:
        return self._cursor.execute(query, **kwargs)


    @property
    def _cursor(self):
        return self.connect.cursor()
