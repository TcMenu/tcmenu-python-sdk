import io

import pytest

from tcmenu.remote.protocol.tag_val_text_parser import TagValTextParser
from tcmenu.remote.protocol.tc_protocol_exception import TcProtocolException


def test_parse_simple_message():
    parser: TagValTextParser = to_buffer("MT=NJ")
    assert "NJ" == parser.get_value("MT")

    with pytest.raises(TcProtocolException):
        parser.get_value("SL")

    with pytest.raises(TcProtocolException):
        parser.get_value_as_int("IN")


def test_parse_example_join():
    parser: TagValTextParser = to_buffer("MT=NJ|CV=ard8_1.0|NM=someone|~")
    assert "NJ" == parser.get_value("MT")
    assert "ard8_1.0" == parser.get_value("CV")
    assert "someone" == parser.get_value("NM")


def test_parse_example_wrong_ending():
    parser: TagValTextParser = to_buffer("MT=NJ|CV=ard8_1.0|NM=~")
    assert "NJ" == parser.get_value("MT")
    assert "ard8_1.0" == parser.get_value("CV")
    assert "~" == parser.get_value("NM")


def test_empty_key_raises_exception():
    with pytest.raises(TcProtocolException):
        to_buffer("MT=NJ|=")


def test_default_value_retrieval():
    parser: TagValTextParser = to_buffer("MT=HB|AB=123|DE=ABCDEF GH|~")
    assert 1000 == parser.get_value_as_int("HI", 1000)
    assert "Abc" == parser.get_value("WO", "Abc")
    assert 123 == parser.get_value_as_int("AB", 42)
    assert "ABCDEF GH" == parser.get_value("DE", "notUsed")


def test_that_pipe_can_be_escaped():
    parser: TagValTextParser = to_buffer("MT=HB|DE=ABCDEF\\|GH|AB=123|~")
    assert "ABCDEF|GH" == parser.get_value("DE")
    assert 123 == parser.get_value_as_int("AB", 42)


def to_buffer(s: str) -> "TagValTextParser":
    return TagValTextParser(io.BytesIO(s.encode()))
