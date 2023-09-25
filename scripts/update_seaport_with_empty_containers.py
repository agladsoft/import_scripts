import os
import sys
from dotenv import load_dotenv
from typing import Optional, Tuple
from clickhouse_connect import get_client
from clickhouse_connect.driver import Client
from clickhouse_connect.driver.query import QueryResult

load_dotenv()


def get_my_env_var(var_name: str) -> str:
    try:
        return os.environ[var_name]
    except KeyError as e:
        raise MissingEnvironmentVariable(f"{var_name} does not exist") from e


class MissingEnvironmentVariable(Exception):
    pass


class SeaportEmptyContainers:

    def __init__(self, logger):
        self.logger = logger
        self.client, self.ref_region = self.connect_to_db()

    def connect_to_db(self) -> Tuple[Client, QueryResult]:
        """
        Connecting to clickhouse.
        :return: Client ClickHouse.
        """
        try:
            client: Client = get_client(host=get_my_env_var('HOST'), database=get_my_env_var('DATABASE'),
                                        username=get_my_env_var('USERNAME_DB'), password=get_my_env_var('PASSWORD'))
            self.logger.info("Successfully connect ot db")
            ref_region: QueryResult = client.query("SELECT * FROM reference_region")
            # Чтобы проверить, есть ли данные. Так как переменная образуется, но внутри нее могут быть ошибки.
            print(ref_region.result_rows[0])
        except Exception as ex_connect:
            self.logger.error(f"Error connection to db {ex_connect}. Type error is {type(ex_connect)}.")
            print("error_connect_db", file=sys.stderr)
            sys.exit(1)
        return client, ref_region

    def get_seaport_for_empty_containers(self, row: dict) -> Optional[str]:
        """
        Find the seaport in the shipper_name field with empty containers.
        :param row: Number of consignment.
        :return: seaport from reference_region.
        """
        index_seaport: int = self.ref_region.column_names.index('seaport')
        index_seaport_unified: int = self.ref_region.column_names.index('seaport_unified')
        index_country: int = self.ref_region.column_names.index('country')
        for seaport in self.ref_region.result_rows:
            if seaport[index_seaport] in row['shipper_name'] \
                    and seaport[index_seaport] != seaport[index_country]:
                self.logger.info(f"Getting seaport {seaport[index_seaport]} "
                                 f"from reference_region by field shipper_name")
                yield seaport[index_seaport_unified]
