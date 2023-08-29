from tcmenu.remote.protocol.correlation_id import CorrelationId


def test_correlation_id_from_string():
    correlation_id1 = CorrelationId.from_string("9")
    correlation_id2 = CorrelationId.from_string("ff")

    assert correlation_id1.correlation == 9
    assert correlation_id2.correlation == 255


def test_correlation_id_str():
    correlation_id1 = CorrelationId.from_string("7f")
    correlation_id2 = CorrelationId(correlation=255)

    assert correlation_id1.__str__() == "0000007f"
    assert correlation_id2.__str__() == "000000ff"


def test_correlation_id_repr():
    correlation_id1 = CorrelationId.from_string("7f")
    correlation_id2 = CorrelationId(correlation=255)

    assert correlation_id1.__repr__() == "Correlation(ID=0000007f)"
    assert correlation_id2.__repr__() == "Correlation(ID=000000ff)"


def test_correlation_id_unique():
    CorrelationId.counter = 0
    correlation_id1 = CorrelationId.new_correlation()
    correlation_id2 = CorrelationId.new_correlation()

    # Make sure correlations are unique
    assert not correlation_id1 == correlation_id2

    # Make sure the counter increments
    assert CorrelationId.counter == 2


def test_correlation_id_and_its_copy_are_equal():
    correlation_id1 = CorrelationId.new_correlation()
    correlation_id2 = CorrelationId.from_string(str(correlation_id1))

    assert correlation_id1 == correlation_id2
