from tcmenu.tagval.protocol.tc_protocol_exception import TcProtocolException


def test_message_only():
    e = TcProtocolException("A test message")
    assert str(e) == "A test message"


def test_message_with_cause():
    cause = Exception("Cause for the error")
    e = TcProtocolException("A test message", cause)
    assert str(e) == "A test message (caused by: Cause for the error)"


def test_cause_attribute():
    cause = Exception("Cause for the error")
    e = TcProtocolException("A test message", cause)
    assert e.cause == cause
