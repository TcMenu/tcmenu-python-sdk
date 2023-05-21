from uuid import UUID, uuid4

from tcmenu.constants import Defaults
from tcmenu.domain.state.menu_tree import MenuTree


class AsyncTcMenuTcpClient:
    """**AsyncTcMenuTcpClient**.

    :param menu_tree: The menu_tree instance to store the menu items retrieved from the remote side.
                      This menu_tree must only be used with one client.
    :param host: (optional) Host IP address or host name.
    :param port: (optional) Port used for communication.
    :param client_name: (optional) Name of this client sent as an identification to the remote end.
    :param uuid: (optional) UUID of this instance. If you don't specify this value, it is generated automatically.
    """
    def __init__(
            self,
            menu_tree: MenuTree,
            host: str = Defaults.HOST,
            port: int = Defaults.TCP_PORT,
            client_name: str = Defaults.CLIENT_NAME,
            uuid: UUID = uuid4()
    ) -> None:
        """Initialize Asyncio TcMenu TCP Client."""
        self._menu_tree = menu_tree
        self._host = host,
        self._port = port,
        self._client_name = client_name
        self._uuid = uuid


class TcMenuTcpClient:
    """**TcMenuTcpClient**.

    :param menu_tree: The menu_tree instance to store the menu items retrieved from the remote side.
                      This menu_tree must only be used with one client.
    :param host: (optional) Host IP address or host name.
    :param port: (optional) Port used for communication.
    :param client_name: (optional) Name of this client sent as an identification to the remote end.
    :param uuid: (optional) UUID of this instance. If you don't specify this value, it is generated automatically.
    """
    def __init__(
            self,
            menu_tree: MenuTree,
            host: str = Defaults.HOST,
            port: int = Defaults.TCP_PORT,
            client_name: str = Defaults.CLIENT_NAME,
            uuid: UUID = uuid4()
    ) -> None:
        """Initialize TcMenu TCP Client."""
        self._menu_tree = menu_tree
        self._host = host,
        self._port = port,
        self._client_name = client_name
        self._uuid = uuid
