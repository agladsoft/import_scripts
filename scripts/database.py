from __init__ import *

load_dotenv()


class DataBase:
    def __init__(self):
        self.client = self.connect_to_db()
        # self.logger = write_log(__file__)

    def connect_to_db(self) -> Tuple[Client, QueryResult, QueryResult]:
        """
        Connecting to clickhouse.
        :return: Client ClickHouse.
        """
        try:
            client: Client = get_client(host=get_my_env_var('HOST'), database=get_my_env_var('DATABASE'),
                                        username=get_my_env_var('USERNAME_DB'), password=get_my_env_var('PASSWORD'))
            # self.logger.info("Successfully connect ot db")
        except Exception as ex_connect:
            # self.logger.error(f"Error connection to db {ex_connect}. Type error is {type(ex_connect)}.")
            sys.exit(1)
        return client

    def get_list_unified_lines(self):
        items = {}
        line_unified_query: QueryResult = self.client.query(
            f"SELECT * FROM reference_lines where line_unified in ('REEL SHIPPING', 'ARKAS',"
            f" 'MSC', 'SINOKOR', 'HEUNG-A LINE', 'SAFETRANS')")
        line_unified = line_unified_query.result_rows
        for data in line_unified:
            key, value = data[1], data[0]
            if key not in items:
                items[key] = [value]
            else:
                items[key].append(value)
        return items
