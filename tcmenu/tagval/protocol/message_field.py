from typing import ClassVar
from dataclasses import dataclass


@dataclass(frozen=True)
class MessageField:
    first_byte: str

    second_byte: str

    _ALL_FIELDS_MAP: ClassVar[dict[str, "MessageField"]] = dict()

    def __post_init__(self):
        if self.id in MessageField._ALL_FIELDS_MAP.keys():
            raise ValueError(f"Duplicate key: {self.id}")
        MessageField._ALL_FIELDS_MAP[self.id] = self

    @property
    def high(self) -> str:
        return self.first_byte

    @property
    def low(self) -> str:
        return self.second_byte

    @property
    def id(self) -> str:
        return f"{self.first_byte}{self.second_byte}"

    @staticmethod
    def from_id(field_id: str) -> "MessageField":
        if field_id in MessageField._ALL_FIELDS_MAP.keys():
            return MessageField._ALL_FIELDS_MAP[field_id]
        else:
            raise ValueError("An unknown message type was generated.")

    def __repr__(self) -> str:
        return f"Field[{self.id}]"
