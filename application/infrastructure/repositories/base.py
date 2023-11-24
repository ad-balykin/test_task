from typing import Any

from pydantic import BaseModel


class BaseRepository:
    def _get_mapping(
            self,
            fields: tuple[str, ...],
            *,
            shift: int = 0,
    ) -> str:
        return ', '.join(
            f'{column} = ${pos}'
            for pos, column in enumerate(fields[shift:], start=1 + shift)
        )

    def _fetch_value(self, source: BaseModel, field_name: str) -> Any:
        value = getattr(source, field_name)

        if isinstance(value, float):
            return str(value)

        return value
