from logging import Logger

from asyncpg import Connection

from application.infrastructure.repositories.base import BaseRepository
from application.domain.models.course import Course


class CourseRepository(BaseRepository):
    table_name = 'public.course'
    fields = (
        'id',
        'exchanger',
        'from_currency',
        'to_currency',
        'value',
        'next_attempt_time',
    )

    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    @property
    def columns(self) -> str:
        return ', '.join(self.fields)

    async def get_all(self, connection: Connection) -> list[Course]:
        sql = f"""
        SELECT {self.columns}
        FROM {self.table_name}
        """

        records = await connection.fetch(sql)

        return [Course(**row) for row in records]

    async def update(self, course: Course, connection: Connection) -> None:
        field_position_mapping = self._get_mapping(self.fields, shift=1)

        sql = f"""
        UPDATE {self.table_name}
        SET {field_position_mapping}
        WHERE id = $1
        """

        query_args = [self._fetch_value(course, field_name) for field_name in self.fields]

        await connection.execute(sql, *query_args)
