# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
"""A Mysql implementation of the PyAirbyte cache.

## Usage Example

```python
from airbyte as ab
from airbyte.caches import MysqlCache

cache = MysqlCache(
    host="myhost",
    port=5432,
    username="myusername",
    password=ab.get_secret("Mysql_PASSWORD"),
    database="mydatabase",
)
```
"""

from __future__ import annotations

from pydantic import PrivateAttr

from airbyte._processors.sql.mysql import MysqlConfig, MysqlSqlProcessor
from airbyte.caches.base import CacheBase


class MysqlCache(MysqlConfig, CacheBase):
    """Configuration for the Mysql cache.

    Also inherits config from the JsonlWriter, which is responsible for writing files to disk.
    """

    _sql_processor_class = PrivateAttr(default=MysqlSqlProcessor)


# Expose the Cache class and also the Config class.
__all__ = ["MysqlCache", "MysqlConfig"]
