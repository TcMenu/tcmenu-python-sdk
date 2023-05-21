"""Constants For TcMenu Server/Client.

This is the single location for storing default
values for the servers and clients.
"""


class Defaults:  # pylint: disable=too-few-public-methods
    """A collection of TcMenu default values.

     .. attribute:: CLIENT_NAME

        The default client name.

     .. attribute:: HOST

        The default TcMenu TCP server address.

     .. attribute:: TCP_PORT

        The default TcMenu TCP server port.

     .. attribute:: HEARTBEAT_FREQUENCY

        The default TagVal heartbeat frequency in seconds.
    """
    CLIENT_NAME = "PythonClient"
    HOST = "127.0.0.1"
    TCP_PORT = 3333
    HEARTBEAT_FREQUENCY = 30
