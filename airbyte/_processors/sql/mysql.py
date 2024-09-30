# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
"""A Mysql implementation of the cache."""

from __future__ import annotations

from overrides import overrides

from airbyte._writers.jsonl import JsonlWriter
from airbyte.secrets.base import SecretString
from airbyte.shared.sql_processor import SqlConfig, SqlProcessorBase


class MysqlConfig(SqlConfig):
    """Configuration for the Mysql cache.

    Also inherits config from the JsonlWriter, which is responsible for writing files to disk.
    """

    host: str
    port: int
    database: str
    username: str
    password: SecretString | str
    quote: str = "`"

    @overrides
    def get_sql_alchemy_url(self) -> SecretString:
        """Return the SQLAlchemy URL to use."""
        return SecretString(
            f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        )

    @overrides
    def get_database_name(self) -> str:
        """Return the name of the database."""
        return self.database


class MysqlSqlProcessor(SqlProcessorBase):
    """A Mysql implementation of the cache.

    Jsonl is used for local file storage before bulk loading.
    Unlike the Snowflake implementation, we can't use the COPY command to load data
    so we insert as values instead.

    TODO: Add optimized bulk load path for Mysql. Could use an alternate file writer
    or another import method. (Relatively low priority, since for now it works fine as-is.)
    """

    supports_merge_insert = False
    file_writer_class = JsonlWriter
    sql_config: MysqlConfig
