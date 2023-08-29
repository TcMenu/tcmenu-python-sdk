import pytest

from tcmenu.remote.protocol.command_protocol import CommandProtocol


def test_valid_command_protocol():
    assert CommandProtocol(0) == CommandProtocol.INVALID
    assert CommandProtocol(0).value == 0
    assert CommandProtocol(1) == CommandProtocol.TAG_VAL_PROTOCOL
    assert CommandProtocol(1).value == 1
    assert CommandProtocol(2) == CommandProtocol.RAW_BIN_PROTOCOL
    assert CommandProtocol(2).value == 2


def test_unsupported_command_protocol():
    with pytest.raises(ValueError):
        CommandProtocol(10)
