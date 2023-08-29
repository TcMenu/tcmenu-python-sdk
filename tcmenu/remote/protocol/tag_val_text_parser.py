import io
from typing import Optional

from tcmenu.remote.protocol.tc_protocol_exception import TcProtocolException
from tcmenu.remote.menu_command_protocol import MenuCommandProtocol


class TagValTextParser:
    """
    This is the parser implementation that understands tag value format and can convert the tags back into
    a series of tags and values suitable for the protocol to decode messages.
    """

    FIELD_TERMINATOR = "|"

    def __init__(self, buffer: io.BytesIO):
        """
        Creates an instance that contains all the tags and values in a map, that can
        then be used to extract the message.
        :param buffer: a buffer containing a message.
        :raises TcProtocolException: if the buffer is invalid.
        """
        self.key_to_value = {}

        found_end = False
        while self._has_remaining(buffer) and not found_end:
            key = self._read_string(buffer)
            if not key:
                raise TcProtocolException("Key is empty in protocol")
            elif key[0] == MenuCommandProtocol.PROTO_END_OF_MSG:
                found_end = True
            else:
                value = self._read_string(buffer)
                if value and value[0] == MenuCommandProtocol.PROTO_END_OF_MSG:
                    found_end = True
                self.key_to_value[key] = value

    @staticmethod
    def _read_string(buffer: io.BytesIO) -> str:
        sb = []

        while True:
            byte = buffer.read(1)
            if not byte:
                break

            ch = byte.decode("utf-8")

            if ch == MenuCommandProtocol.PROTO_END_OF_MSG:
                return "\u0002"
            elif ch == "\\":
                # special escape case allows anything to be sent
                ch = buffer.read(1).decode("utf-8")
                sb.append(ch)
            elif ch == "=" or ch == TagValTextParser.FIELD_TERMINATOR:
                # end of current token
                return "".join(sb)
            else:
                # within current token
                sb.append(ch)

        return "".join(sb)

    def get_value(self, key_msg_type: str, default_val: Optional[str] = None) -> str:
        """
        Gets the value associated with the key from the message. This version raises an exception
        if the key is not available and should be used for mandatory fields.
        :param key_msg_type: the key to obtain.
        :param default_val: default value.
        :return: the associated value.
        """
        if default_val is not None or key_msg_type in self.key_to_value:
            return self.key_to_value.get(key_msg_type, default_val)
        else:
            raise TcProtocolException(f"Key {key_msg_type} doesn't exist in {self.key_to_value}")

    def get_value_as_int(self, key_id_field: str, default_val: Optional[int] = None) -> int:
        """
        Calls the get_value method first and the converts to an integer.
        :param key_id_field: the key to obtain.
        :param default_val: default value.
        :return: the integer value associated.
        """
        return int(self.get_value(key_id_field, default_val))

    def __str__(self):
        return " ".join(f"[Key='{k}', val='{v}']" for k, v in self.key_to_value.items())

    @staticmethod
    def _has_remaining(buffer: io.BytesIO) -> bool:
        return buffer.tell() < len(buffer.getvalue())
