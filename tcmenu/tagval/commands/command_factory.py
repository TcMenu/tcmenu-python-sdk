from typing import Optional, Union
from uuid import UUID

from tcmenu.domain.menu_items import (
    AnalogMenuItem,
    RuntimeListMenuItem,
    SubMenuItem,
    EnumMenuItem,
    BooleanMenuItem,
    FloatMenuItem,
    ActionMenuItem,
    EditableTextMenuItem,
    EditableLargeNumberMenuItem,
    MenuItem,
    ScrollChoiceMenuItem,
    Rgb32MenuItem,
)
from tcmenu.domain.state.current_scroll_position import CurrentScrollPosition
from tcmenu.domain.state.list_response import ListResponse
from tcmenu.domain.state.portable_color import PortableColor
from tcmenu.tagval.commands.ack_status import AckStatus
from tcmenu.tagval.commands.dialog_mode import DialogMode
from tcmenu.tagval.commands.menu_acknowledgement_command import MenuAcknowledgementCommand
from tcmenu.tagval.commands.menu_bootstrap_command import MenuBootstrapCommand
from tcmenu.tagval.commands.menu_button_type import MenuButtonType
from tcmenu.tagval.commands.menu_boot_commands import (
    MenuAnalogBootCommand,
    MenuRuntimeListBootCommand,
    MenuSubBootCommand,
    MenuEnumBootCommand,
    MenuBooleanBootCommand,
    MenuFloatBootCommand,
    MenuActionBootCommand,
    MenuTextBootCommand,
    MenuLargeNumBootCommand,
    MenuScrollChoiceBootCommand,
    MenuRgb32BootCommand,
)
from tcmenu.tagval.commands.menu_change_command import MenuChangeCommand
from tcmenu.tagval.commands.menu_dialog_command import MenuDialogCommand
from tcmenu.tagval.commands.menu_heartbeat_command import MenuHeartbeatCommand
from tcmenu.tagval.commands.menu_join_command import MenuJoinCommand
from tcmenu.tagval.commands.menu_pairing_command import MenuPairingCommand
from tcmenu.tagval.protocol.api_platform import ApiPlatform
from tcmenu.tagval.protocol.correlation_id import CorrelationId
from tcmenu.tagval.protocol.protocol_util import ProtocolUtil


class CommandFactory:
    """
    These static helper methods are the preferred way to create command message that can be sent and received from
    a tagval connection. Each protocol can convert sent and received messages into this form.
    """

    @staticmethod
    def new_join_command(name: str, uuid: Optional[UUID] = None) -> MenuJoinCommand:
        """
        Create a new join command. You can either provide a fixed UUID
        or a random UUID will be generated for you.

        :param name: the name that the tagval will show for the connection.
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
    def new_bootstrap_command(boot_type: MenuBootstrapCommand.BootType) -> MenuBootstrapCommand:
        """
        Create a new bootstrap message either to indicate the bootstrap start or end.
        :param boot_type: one of the enum values allowed.
        :return: bootstrap message.
        """
        return MenuBootstrapCommand(boot_type)

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
        parent_id: int, item: RuntimeListMenuItem, current_value: tuple[str, ...]
    ) -> MenuRuntimeListBootCommand:
        """
        Create a new runtime list boot command.
        :param parent_id: the parent onto which this will be placed.
        :param item: the item itself.
        :param current_value: the current value.
        :return: a new runtime list boot command.
        """
        return MenuRuntimeListBootCommand(sub_menu_id=parent_id, menu_item=item, current_value=current_value)

    @staticmethod
    def new_sub_menu_boot_command(parent_id: int, item: SubMenuItem) -> MenuSubBootCommand:
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
    def new_menu_boolean_boot_command(
        parent_id: int, item: BooleanMenuItem, current_value: bool
    ) -> MenuBooleanBootCommand:
        """
        Create a new boolean bootstrap command.
        :param parent_id: the parent onto which the item will be placed.
        :param item: the item itself.
        :param current_value: the current value.
        :return: a new boolean boot command.
        """
        return MenuBooleanBootCommand(sub_menu_id=parent_id, menu_item=item, current_value=current_value)

    @staticmethod
    def new_menu_float_boot_command(parent_id: int, item: FloatMenuItem, current_value: float) -> MenuFloatBootCommand:
        """
        Create a new float bootstrap command.
        :param parent_id: the parent onto which the item will be placed.
        :param item: the item itself.
        :param current_value: the current value.
        :return: a new float boot command.
        """
        return MenuFloatBootCommand(sub_menu_id=parent_id, menu_item=item, current_value=current_value)

    @staticmethod
    def new_menu_action_boot_command(parent_id: int, item: ActionMenuItem) -> MenuActionBootCommand:
        """
        Create a new action bootstrap command.
        :param parent_id: the parent onto which the item will be placed.
        :param item: the item itself.
        :return: a new action boot command.
        """
        return MenuActionBootCommand(sub_menu_id=parent_id, menu_item=item, current_value=False)

    @staticmethod
    def new_menu_text_boot_command(
        parent_id: int, item: EditableTextMenuItem, current_value: str
    ) -> MenuTextBootCommand:
        """
        Create a new text bootstrap command.
        :param parent_id: the parent onto which the item will be placed.
        :param item: the item itself.
        :param current_value: the current value.
        :return: a new text boot command.
        """
        return MenuTextBootCommand(sub_menu_id=parent_id, menu_item=item, current_value=current_value)

    @staticmethod
    def new_menu_large_item_boot_command(
        parent_id: int, item: EditableLargeNumberMenuItem, current_value: int
    ) -> MenuLargeNumBootCommand:
        """
        Create a new large number bootstrap command.
        :param parent_id: the parent onto which the item will be placed.
        :param item: the item itself.
        :param current_value: the current value.
        :return: a new large number boot command.
        """
        return MenuLargeNumBootCommand(sub_menu_id=parent_id, menu_item=item, current_value=current_value)

    @staticmethod
    def new_menu_scroll_choice_boot_command(
        parent_id: int, item: ScrollChoiceMenuItem, current_value: CurrentScrollPosition
    ) -> MenuScrollChoiceBootCommand:
        """
        Create a new float bootstrap command.
        :param parent_id: the parent onto which the item will be placed.
        :param item: the item itself.
        :param current_value: the current value.
        :return: a new float boot command.
        """
        return MenuScrollChoiceBootCommand(sub_menu_id=parent_id, menu_item=item, current_value=current_value)

    @staticmethod
    def new_menu_rgb32_boot_command(
        parent_id: int, item: Rgb32MenuItem, current_value: PortableColor
    ) -> MenuRgb32BootCommand:
        """
        Create a new float bootstrap command.
        :param parent_id: the parent onto which the item will be placed.
        :param item: the item itself.
        :param current_value: the current value.
        :return: a new float boot command.
        """
        return MenuRgb32BootCommand(sub_menu_id=parent_id, menu_item=item, current_value=current_value)

    @staticmethod
    def new_delta_menu_change_command(correlation_id: CorrelationId, item: Union[MenuItem, int], value: int):
        """
        Creates a new delta change command given the menu item and the delta change in value.
        :param correlation_id: a correlation ID that will be returned in the subsequent acknowledgement.
        :param item: the item (or its ID) for which to send.
        :param value: the change in value as a delta of the current value.
        :return: a new change message.
        """
        if isinstance(item, MenuItem):
            item_id = item.id
        else:
            item_id = item

        return MenuChangeCommand(
            correlation_id=correlation_id,
            menu_item_id=item_id,
            change_type=MenuChangeCommand.ChangeType.DELTA,
            value=str(value),
        )

    @staticmethod
    def new_absolute_menu_change_command(correlation_id: CorrelationId, item: Union[MenuItem, int], value: int):
        """
        Creates a new absolute change command given the menu item and the absolute change in value.
        :param correlation_id: a correlation ID that will be returned in the subsequent acknowledgement.
        :param item: the item (or its ID) for which to send.
        :param value: the new value.
        :return: a new change message.
        """
        if isinstance(item, MenuItem):
            item_id = item.id
        else:
            item_id = item

        return MenuChangeCommand(
            correlation_id=correlation_id,
            menu_item_id=item_id,
            change_type=MenuChangeCommand.ChangeType.ABSOLUTE,
            value=str(value),
        )

    @staticmethod
    def new_list_response_menu_change_command(
        correlation_id: CorrelationId, item: Union[MenuItem, int], value: ListResponse
    ):
        """
        Creates a new change command that represents a list item either being selected or invoked.
        :param correlation_id: a correlation ID that will be returned in the subsequent acknowledgement.
        :param item: the item (or its ID) for which to send.
        :param value: the new value, must be a ListResponse.
        :return: a new change message.
        """
        if isinstance(item, MenuItem):
            item_id = item.id
        else:
            item_id = item

        return MenuChangeCommand(
            correlation_id=correlation_id,
            menu_item_id=item_id,
            change_type=MenuChangeCommand.ChangeType.LIST_STATE_CHANGE,
            value=str(value),
        )

    @staticmethod
    def new_absolute_list_menu_change_command(
        correlation_id: CorrelationId, item: Union[MenuItem, int], values: tuple[str, ...]
    ):
        """
        Creates a new change command that represents a list item either being selected or invoked.
        :param correlation_id: a correlation ID that will be returned in the subsequent acknowledgement.
        :param item: the item (or its ID) for which to send.
        :param values: the new value.
        :return: a new change message.
        """
        if isinstance(item, MenuItem):
            item_id = item.id
        else:
            item_id = item

        return MenuChangeCommand(
            correlation_id=correlation_id,
            menu_item_id=item_id,
            change_type=MenuChangeCommand.ChangeType.ABSOLUTE_LIST,
            value=values,
        )
