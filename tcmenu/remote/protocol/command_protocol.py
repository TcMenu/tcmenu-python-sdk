from enum import Enum


class CommandProtocol(Enum):
    INVALID = 0
    TAG_VAL_PROTOCOL = 1
    RAW_BIN_PROTOCOL = 2

    @property
    def protocol_num(self) -> bytes:
        return (self.value & 0xFF).to_bytes(1, "big")
