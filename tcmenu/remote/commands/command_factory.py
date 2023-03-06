from typing import Optional
from uuid import UUID

from tcmenu.domain.menu_items import AnalogMenuItem, RuntimeListMenuItem, SubMenuItem, EnumMenuItem, BooleanMenuItem, \
    FloatMenuItem
from tcmenu.remote.commands.ack_status import AckStatus
from tcmenu.remote.commands.dialog_mode import DialogMode
from tcmenu.remote.commands.menu_button_type import MenuButtonType
from tcmenu.remote.commands.menu_commands import (
    MenuJoinCommand,
    MenuHeartbeatCommand,
    MenuAcknowledgementCommand,
    MenuPairingCommand,
    MenuDialogCommand,
    MenuBootstrapCommand,
    MenuAnalogBootCommand,
    MenuRuntimeListBootCommand, MenuSubBootCommand, MenuEnumBootCommand, MenuBooleanBootCommand, MenuFloatBootCommand,
)
from tcmenu.remote.protocol.api_platform import ApiPlatform
from tcmenu.remote.protocol.correlation_id import CorrelationId
from tcmenu.remote.protocol.protocol_util import ProtocolUtil


class CommandFactory:
    """
    These static helper methods are the preferred way to create command message that can be sent and received from
    a remote connection. Each protocol can convert sent and received messages into this form.
    """

    @staticmethod
    def new_join_command(name: str, uuid: Optional[UUID] = None) -> MenuJoinCommand:
        """
        Create a new join command. You can either provide a fixed UUID
        or a random UUID will be generated for you.

        :param name: the name that the remote will show for the connection.
        :param uuid: optional; the UUID that identifies our client.
        :return: join command.
        """
        if not uuid:
            return MenuJoinCommand(
                my_name=name, platform=ApiPlatform.PYTHON_API, api_version=ProtocolUtil.get_version_from_properties()
            )
        else:
            return MenuJoinCommand(
                my_name=name,
                platform=ApiPlatform.PYTHON_API,
                api_version=ProtocolUtil.get_version_from_properties(),
                app_uuid=uuid,
            )

    @staticmethod
    def new_heartbeat_command(frequency: int, mode: MenuHeartbeatCommand.HeartbeatMode) -> MenuHeartbeatCommand:
        """
        Create a new heartbeat message with the frequency specified.
        :param frequency: the frequency.
        :param mode: heartbeat mode.
        :return: heartbeat command.
        """
        return MenuHeartbeatCommand(frequency, mode)

    @staticmethod
    def new_acknowledgement_command(correlation_id: CorrelationId, status: AckStatus) -> MenuAcknowledgementCommand:
        """
        Create an acknowledgement message for a given correlation and status.
        :param correlation_id: the correlation.
        :param status: the status.
        :return: the message
        """
        return MenuAcknowledgementCommand(correlation_id, status)

    @staticmethod
    def new_pairing_command(name: str, uuid: UUID) -> MenuPairingCommand:
        """
        Create a new pairing command.
        :param name: Name of the device initializing the pairing request.
        :param uuid: ID of the device.
        :return: pairing command.
        """
        return MenuPairingCommand(name, uuid)

    @staticmethod
    def new_dialog_command(
        mode: DialogMode,
        header: str,
        message: str,
        button1: MenuButtonType,
        button2: MenuButtonType,
        correlation_id: CorrelationId,
    ) -> MenuDialogCommand:
        """
        Create a new dialog command.
        """
        return MenuDialogCommand(mode, header, message, button1, button2, correlation_id)

    @staticmethod
    def new_bootstrap_command(type: MenuBootstrapCommand.BootType) -> MenuBootstrapCommand:
        """
        Create a new bootstrap message either to indicate the bootstrap start or end.
        :param type: one of the enum values allowed.
        :return: bootstrap message.
        """
        return MenuBootstrapCommand(type)

    @staticmethod
    def new_analog_boot_command(parent_id: int, item: AnalogMenuItem, current_value: int) -> MenuAnalogBootCommand:
        """
        Create a new analog bootstrap command.
        :param parent_id: the parent onto which the item will be placed.
        :param item: the item itself.
        :param current_value: the current value.
        :return: a new analog boot command.
        """
        return MenuAnalogBootCommand(sub_menu_id=parent_id, menu_item=item, current_value=current_value)

    @staticmethod
    def new_runtime_list_boot_command(
        parent_id: int, item: RuntimeListMenuItem, value: tuple[str]
    ) -> MenuRuntimeListBootCommand:
        """
        Create a new runtime list boot command.
        :param parent_id: the parent onto which this will be placed.
        :param item: the item itself.
        :param value: the current value.
        :return: a new runtime list boot command.
        """
        return MenuRuntimeListBootCommand(sub_menu_id=parent_id, menu_item=item, current_value=value)

    @staticmethod
    def new_menu_sub_boot_command(parent_id: int, item: SubMenuItem) -> MenuSubBootCommand:
        """
        Create a new submenu bootstrap command.
        :param parent_id: the parent onto which the item will be placed.
        :param item: the item itself.
        :return: a new submenu boot command.
        """
        return MenuSubBootCommand(sub_menu_id=parent_id, menu_item=item, current_value=False)

    @staticmethod
    def new_menu_enum_boot_command(parent_id: int, item: EnumMenuItem, current_value: int) -> MenuEnumBootCommand:
        """
        Create a new enum bootstrap command.
        :param parent_id: the parent onto which the item will be placed.
        :param item: the item itself.
        :param current_value: the current value.
        :return: a new enum boot command.
        """
        return MenuEnumBootCommand(sub_menu_id=parent_id, menu_item=item, current_value=current_value)

    @staticmethod
    def new_menu_boolean_boot_command(parent_id: int, item: BooleanMenuItem, current_value: int) -> MenuBooleanBootCommand:
        """
        Create a new boolean bootstrap command.
        :param parent_id: the parent onto which the item will be placed.
        :param item: the item itself.
        :param current_value: the current value.
        :return: a new boolean boot command.
        """
        return MenuBooleanBootCommand(sub_menu_id=parent_id, menu_item=item, current_value=current_value)

    @staticmethod
    def new_menu_float_boot_command(parent_id: int, item: FloatMenuItem, current_value: int) -> MenuFloatBootCommand:
        """
        Create a new float bootstrap command.
        :param parent_id: the parent onto which the item will be placed.
        :param item: the item itself.
        :param current_value: the current value.
        :return: a new float boot command.
        """
        return MenuFloatBootCommand(sub_menu_id=parent_id, menu_item=item, current_value=current_value)

