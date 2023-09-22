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
            ref_region: QueryResult = client.query("SELECT * FROM reference_is_empty")
        except Exception as ex_connect:
            self.logger.error(f"Error connection to db {ex_connect}. Type error is {type(ex_connect)}.")
            print("error_connect_db", file=sys.stderr)
            sys.exit(1)
        return client, ref_region

    def get_seaport_for_empty_containers(self, consignment: str) -> Optional[str]:
        """
        Find the seaport in the shipper_name field with empty containers.
        :param consignment: Number of consignment.
        :return: seaport from reference_region.
        """
        rows: QueryResult = self.client.query(f"SELECT consignment, shipper_name FROM import_enriched "
                                              f"WHERE consignment='{consignment}' and is_empty = true "
                                              f"GROUP BY consignment, shipper_name")
        self.logger.info("Got data from sql-query")
        index_shipper: int = rows.column_names.index('shipper_name')
        index_seaport: int = self.ref_region.column_names.index('seaport')
        index_country: int = self.ref_region.column_names.index('country')
        for row in rows.result_rows:
            for seaport in self.ref_region.result_rows:
                if seaport[index_seaport] in row[index_shipper].split() \
                        and seaport[index_seaport] != seaport[index_country]:
                    self.logger.info(f"Getting seaport {seaport[index_seaport]} "
                                     f"from reference_region by field shipper_name")
                    yield seaport[index_seaport]
