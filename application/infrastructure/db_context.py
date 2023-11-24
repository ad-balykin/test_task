from logging import Logger
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import asyncpg
from asyncpg import Connection
from asyncpg.transaction import Transaction

from application.config import AppConfig


class DBContext:
    def __init__(self, connection: Connection, transaction: Transaction) -> None:
        self.connection = connection
        self.transaction = transaction


class DBContextFactory:
    def __init__(
            self,
            logger: Logger,
            config: AppConfig,
    ) -> None:
        self._logger = logger

        self._connection_pool = asyncpg.create_pool(
            config.postgres_config.dsn,
            min_size=config.postgres_config.min_size,
            max_size=config.postgres_config.max_size,
        )

    @asynccontextmanager
    async def create_context(self) -> AsyncGenerator[DBContext, None]:
        await self._connection_pool._async__init__()

        async with self._connection_pool.acquire() as connection:
            async with connection.transaction() as transaction:
                yield DBContext(connection=connection, transaction=transaction)
