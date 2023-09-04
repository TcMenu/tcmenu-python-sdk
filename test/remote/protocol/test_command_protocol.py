import pytest

from tcmenu.remote.protocol.command_protocol import CommandProtocol


def test_valid_command_protocol():
    assert CommandProtocol(0) == CommandProtocol.INVALID
    assert CommandProtocol(0).value == 0
    assert CommandProtocol(0).protocol_num == b"\x00"
    assert CommandProtocol(1) == CommandProtocol.TAG_VAL_PROTOCOL
    assert CommandProtocol(1).value == 1
    assert CommandProtocol(1).protocol_num == b"\x01"
    assert CommandProtocol(2) == CommandProtocol.RAW_BIN_PROTOCOL
    assert CommandProtocol(2).value == 2
    assert CommandProtocol(2).protocol_num == b"\x02"


def test_unsupported_command_protocol():
    with pytest.raises(ValueError):
        CommandProtocol(10)


def test_protocol_num_unsupported_command():
    with pytest.raises(ValueError):
        # noinspection PyStatementEffect
        CommandProtocol(10).protocol_num


def test_from_protocol_id():
    """
    Always expect RAW protocol when the ID doesn't match with TAG_VAL.
    """
    assert CommandProtocol.RAW_BIN_PROTOCOL == CommandProtocol.from_protocol_id(0)
    assert CommandProtocol.TAG_VAL_PROTOCOL == CommandProtocol.from_protocol_id(1)
    assert CommandProtocol.RAW_BIN_PROTOCOL == CommandProtocol.from_protocol_id(100)
