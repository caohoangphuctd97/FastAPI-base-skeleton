from dataclasses import dataclass, field
from typing import Generic, Optional, Sequence, TypeVar
from uuid import UUID

T = TypeVar("T")


@dataclass
class PagedResultSet(Generic[T]):
    """Results wrapper for SqlA >= 1.4

    Wraps results for consumption by pagination aware callers.
    """

    offset: int
    count: int = field(init=False)
    total: int
    records: Sequence[T]

    def __post_init__(self) -> None:
        self.count = len(self.records)


class ItemDoesntExist(Exception):
    def __init__(self, type_: str, id_: Optional[UUID] = None):
        self.id_ = id_
        self.type_ = type_
        self.detail = f"Item {self.type_} with id {self.id_} not found."
        super().__init__(self.detail)


class ItemHasConstraintError(Exception):
    def __init__(self, type_: str, detail_error: str):
        self.type_ = type_
        self.detail = f"Item {self.type_} has error. {detail_error}"
        super().__init__(self.detail)
