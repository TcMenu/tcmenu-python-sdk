from tcmenu.remote.commands.ack_status import AckStatus


def test_ack_status_warning():
    ack_status = AckStatus.VALUE_RANGE_WARNING

    assert ack_status.description == "Value out of range"
    assert ack_status.status_code < 0
    assert ack_status.is_error() is False


def test_ack_status_success():
    ack_status = AckStatus.SUCCESS

    assert ack_status.description == "OK"
    assert ack_status.status_code == 0
    assert ack_status.is_error() is False


def test_ack_status_error():
    ack_status = AckStatus.INVALID_CREDENTIALS

    assert ack_status.description == "Invalid Credentials"
    assert ack_status.status_code > 0
    assert ack_status.is_error() is True
