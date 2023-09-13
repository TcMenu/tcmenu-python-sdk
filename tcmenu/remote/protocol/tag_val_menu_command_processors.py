import io
import uuid
from typing import Any

from tcmenu.domain.edit_item_type import EditItemType
from tcmenu.domain.menu_items import (
    AnalogMenuItem,
    FloatMenuItem,
    RuntimeListMenuItem,
    EditableTextMenuItem,
    EnumMenuItem,
    EditableLargeNumberMenuItem,
    SubMenuItem,
    Rgb32MenuItem,
    ScrollChoiceMenuItem,
    ActionMenuItem,
    BooleanMenuItem,
)
from tcmenu.domain.state.current_scroll_position import CurrentScrollPosition
from tcmenu.domain.state.list_response import ListResponse
from tcmenu.domain.state.portable_color import PortableColor
from tcmenu.remote.commands.ack_status import AckStatus
from tcmenu.remote.commands.command_factory import CommandFactory
from tcmenu.remote.commands.dialog_mode import DialogMode
from tcmenu.remote.commands.menu_acknowledgement_command import MenuAcknowledgementCommand
from tcmenu.remote.commands.menu_boot_commands import (
    MenuAnalogBootCommand,
    MenuSubBootCommand,
    MenuEnumBootCommand,
    MenuBooleanBootCommand,
    MenuLargeNumBootCommand,
    MenuTextBootCommand,
    MenuFloatBootCommand,
    MenuActionBootCommand,
    MenuRuntimeListBootCommand,
    MenuRgb32BootCommand,
    MenuScrollChoiceBootCommand,
    BootItemMenuCommand,
)
from tcmenu.remote.commands.menu_bootstrap_command import MenuBootstrapCommand
from tcmenu.remote.commands.menu_button_type import MenuButtonType
from tcmenu.remote.commands.menu_change_command import MenuChangeCommand
from tcmenu.remote.commands.menu_command_type import MenuCommandType
from tcmenu.remote.commands.menu_dialog_command import MenuDialogCommand
from tcmenu.remote.commands.menu_heartbeat_command import MenuHeartbeatCommand
from tcmenu.remote.commands.menu_join_command import MenuJoinCommand
from tcmenu.remote.commands.menu_pairing_command import MenuPairingCommand
from tcmenu.remote.protocol.correlation_id import CorrelationId
from tcmenu.remote.protocol.protocol_util import ProtocolUtil
from tcmenu.remote.protocol.tag_val_menu_fields import TagValMenuFields
from tcmenu.remote.protocol.tag_val_text_parser import TagValTextParser


class TagValMenuCommandProcessors:
    # noinspection PyUnresolvedReferences
    @staticmethod
    def add_handlers_to_protocol(proto: "ConfigurableProtocolConverter"):
        # Input processors
        proto.add_tag_val_in_processor(MenuCommandType.JOIN.message_field, TagValMenuCommandProcessors._process_join)
        proto.add_tag_val_in_processor(
            MenuCommandType.HEARTBEAT.message_field, TagValMenuCommandProcessors._process_heartbeat
        )
        proto.add_tag_val_in_processor(
            MenuCommandType.BOOTSTRAP.message_field, TagValMenuCommandProcessors._process_bootstrap
        )
        proto.add_tag_val_in_processor(
            MenuCommandType.ANALOG_BOOT_ITEM.message_field, TagValMenuCommandProcessors._process_analog_boot_item
        )
        proto.add_tag_val_in_processor(
            MenuCommandType.SUBMENU_BOOT_ITEM.message_field, TagValMenuCommandProcessors._process_sub_menu_boot_item
        )
        proto.add_tag_val_in_processor(
            MenuCommandType.ENUM_BOOT_ITEM.message_field, TagValMenuCommandProcessors._process_enum_boot_item
        )
        proto.add_tag_val_in_processor(
            MenuCommandType.BOOLEAN_BOOT_ITEM.message_field, TagValMenuCommandProcessors._process_boolean_boot_item
        )
        proto.add_tag_val_in_processor(
            MenuCommandType.LARGE_NUM_BOOT_ITEM.message_field, TagValMenuCommandProcessors._process_large_num_boot_item
        )
        proto.add_tag_val_in_processor(
            MenuCommandType.CHANGE_INT_FIELD.message_field, TagValMenuCommandProcessors._process_item_change
        )
        proto.add_tag_val_in_processor(
            MenuCommandType.TEXT_BOOT_ITEM.message_field, TagValMenuCommandProcessors._process_text_boot_item
        )
        proto.add_tag_val_in_processor(
            MenuCommandType.FLOAT_BOOT_ITEM.message_field, TagValMenuCommandProcessors._process_float_boot_item
        )
        proto.add_tag_val_in_processor(
            MenuCommandType.ACTION_BOOT_ITEM.message_field, TagValMenuCommandProcessors._process_action_boot_item
        )
        proto.add_tag_val_in_processor(
            MenuCommandType.RUNTIME_LIST_BOOT.message_field, TagValMenuCommandProcessors._process_runtime_list_boot_item
        )
        proto.add_tag_val_in_processor(
            MenuCommandType.BOOT_RGB_COLOR.message_field, TagValMenuCommandProcessors._process_runtime_rgb_color_item
        )
        proto.add_tag_val_in_processor(
            MenuCommandType.BOOT_SCROLL_CHOICE.message_field, TagValMenuCommandProcessors._process_runtime_scroll_choice
        )
        proto.add_tag_val_in_processor(
            MenuCommandType.ACKNOWLEDGEMENT.message_field, TagValMenuCommandProcessors._process_acknowledgement
        )
        proto.add_tag_val_in_processor(
            MenuCommandType.PAIRING_REQUEST.message_field, TagValMenuCommandProcessors._process_pairing_request
        )
        proto.add_tag_val_in_processor(
            MenuCommandType.DIALOG_UPDATE.message_field, TagValMenuCommandProcessors._process_dialog_update
        )

        # Output processors
        proto.add_tag_val_out_processor(
            MenuCommandType.JOIN.message_field, TagValMenuCommandProcessors._write_join, MenuJoinCommand
        )
        proto.add_tag_val_out_processor(
            MenuCommandType.HEARTBEAT.message_field, TagValMenuCommandProcessors._write_heartbeat, MenuHeartbeatCommand
        )
        proto.add_tag_val_out_processor(
            MenuCommandType.BOOTSTRAP.message_field, TagValMenuCommandProcessors._write_bootstrap, MenuBootstrapCommand
        )
        proto.add_tag_val_out_processor(
            MenuCommandType.ANALOG_BOOT_ITEM.message_field,
            TagValMenuCommandProcessors._write_analog_boot_item,
            MenuAnalogBootCommand,
        )
        proto.add_tag_val_out_processor(
            MenuCommandType.SUBMENU_BOOT_ITEM.message_field,
            TagValMenuCommandProcessors._write_sub_menu_boot_item,
            MenuSubBootCommand,
        )
        proto.add_tag_val_out_processor(
            MenuCommandType.ENUM_BOOT_ITEM.message_field,
            TagValMenuCommandProcessors._write_enum_boot_item,
            MenuEnumBootCommand,
        )
        proto.add_tag_val_out_processor(
            MenuCommandType.BOOLEAN_BOOT_ITEM.message_field,
            TagValMenuCommandProcessors._write_boolean_boot_item,
            MenuBooleanBootCommand,
        )
        proto.add_tag_val_out_processor(
            MenuCommandType.LARGE_NUM_BOOT_ITEM.message_field,
            TagValMenuCommandProcessors._write_large_num_boot_item,
            MenuLargeNumBootCommand,
        )
        proto.add_tag_val_out_processor(
            MenuCommandType.CHANGE_INT_FIELD.message_field,
            TagValMenuCommandProcessors._write_item_change,
            MenuChangeCommand,
        )
        proto.add_tag_val_out_processor(
            MenuCommandType.TEXT_BOOT_ITEM.message_field,
            TagValMenuCommandProcessors._write_text_boot_item,
            MenuTextBootCommand,
        )
        proto.add_tag_val_out_processor(
            MenuCommandType.FLOAT_BOOT_ITEM.message_field,
            TagValMenuCommandProcessors._write_float_boot_item,
            MenuFloatBootCommand,
        )
        proto.add_tag_val_out_processor(
            MenuCommandType.ACTION_BOOT_ITEM.message_field,
            TagValMenuCommandProcessors._write_action_boot_item,
            MenuActionBootCommand,
        )
        proto.add_tag_val_out_processor(
            MenuCommandType.RUNTIME_LIST_BOOT.message_field,
            TagValMenuCommandProcessors._write_runtime_list_boot_item,
            MenuRuntimeListBootCommand,
        )
        proto.add_tag_val_out_processor(
            MenuCommandType.BOOT_RGB_COLOR.message_field,
            TagValMenuCommandProcessors._write_runtime_rgb_color_item,
            MenuRgb32BootCommand,
        )
        proto.add_tag_val_out_processor(
            MenuCommandType.BOOT_SCROLL_CHOICE.message_field,
            TagValMenuCommandProcessors._write_runtime_scroll_choice,
            MenuScrollChoiceBootCommand,
        )
        proto.add_tag_val_out_processor(
            MenuCommandType.ACKNOWLEDGEMENT.message_field,
            TagValMenuCommandProcessors._write_acknowledgement,
            MenuAcknowledgementCommand,
        )
        proto.add_tag_val_out_processor(
            MenuCommandType.PAIRING_REQUEST.message_field,
            TagValMenuCommandProcessors._write_pairing_request,
            MenuPairingCommand,
        )
        proto.add_tag_val_out_processor(
            MenuCommandType.DIALOG_UPDATE.message_field,
            TagValMenuCommandProcessors._write_dialog_update,
            MenuDialogCommand,
        )

    @staticmethod
    def _process_join(parser: TagValTextParser) -> MenuJoinCommand:
        uuid_str: str = parser.get_value(TagValMenuFields.KEY_UUID_FIELD.value, "")
        uuid_val: uuid.UUID = uuid.UUID(uuid_str) if len(uuid_str) > 0 else uuid.uuid4()

        return MenuJoinCommand(
            my_name=parser.get_value(TagValMenuFields.KEY_NAME_FIELD.value),
            api_version=parser.get_value_as_int(TagValMenuFields.KEY_VER_FIELD.value),
            platform=ProtocolUtil.from_key_to_api_platform(
                parser.get_value_as_int(TagValMenuFields.KEY_PLATFORM_ID.value)
            ),
            app_uuid=uuid_val,
            serial_number=parser.get_value_as_int(TagValMenuFields.KEY_SERIAL_NO.value, 0),
        )

    @staticmethod
    def _process_heartbeat(parser: TagValTextParser) -> MenuHeartbeatCommand:
        return CommandFactory.new_heartbeat_command(
            frequency=parser.get_value_as_int(TagValMenuFields.HB_FREQUENCY_FIELD.value, 10000),
            mode=MenuHeartbeatCommand.from_id(parser.get_value_as_int(TagValMenuFields.HB_MODE_FIELD.value, 0)),
        )

    @staticmethod
    def _process_bootstrap(parser: TagValTextParser) -> MenuBootstrapCommand:
        boot_type = MenuBootstrapCommand.BootType[parser.get_value(TagValMenuFields.KEY_BOOT_TYPE_FIELD.value)]
        return MenuBootstrapCommand(boot_type=boot_type)

    @staticmethod
    def _process_analog_boot_item(parser: TagValTextParser) -> MenuAnalogBootCommand:
        item: AnalogMenuItem = AnalogMenuItem(
            id=parser.get_value_as_int(TagValMenuFields.KEY_ID_FIELD.value),
            divisor=parser.get_value_as_int(TagValMenuFields.KEY_ANALOG_DIVISOR_FIELD.value),
            max_value=parser.get_value_as_int(TagValMenuFields.KEY_ANALOG_MAX_FIELD.value),
            eeprom_address=parser.get_value_as_int(TagValMenuFields.KEY_EEPROM_FIELD.value, 0),
            offset=parser.get_value_as_int(TagValMenuFields.KEY_ANALOG_OFFSET_FIELD.value),
            step=parser.get_value_as_int(TagValMenuFields.KEY_ANALOG_STEP_FIELD.value, 1),
            unit_name=parser.get_value(TagValMenuFields.KEY_ANALOG_UNIT_FIELD.value),
            name=parser.get_value(TagValMenuFields.KEY_NAME_FIELD.value),
            read_only=parser.get_value_as_int(TagValMenuFields.KEY_READONLY_FIELD.value) != 0,
            visible=parser.get_value_as_int(TagValMenuFields.KEY_VISIBLE_FIELD.value, 1) != 0,
        )

        parent_id: int = parser.get_value_as_int(TagValMenuFields.KEY_PARENT_ID_FIELD.value)
        current_val: int = parser.get_value_as_int(TagValMenuFields.KEY_CURRENT_VAL.value)

        return CommandFactory.new_analog_boot_command(parent_id=parent_id, item=item, current_value=current_val)

    @staticmethod
    def _process_sub_menu_boot_item(parser: TagValTextParser) -> MenuSubBootCommand:
        item: SubMenuItem = SubMenuItem(
            id=parser.get_value_as_int(TagValMenuFields.KEY_ID_FIELD.value),
            eeprom_address=parser.get_value_as_int(TagValMenuFields.KEY_EEPROM_FIELD.value, 0),
            name=parser.get_value(TagValMenuFields.KEY_NAME_FIELD.value),
        )

        parent_id: int = parser.get_value_as_int(TagValMenuFields.KEY_PARENT_ID_FIELD.value)

        return CommandFactory.new_sub_menu_boot_command(parent_id=parent_id, item=item)

    @staticmethod
    def _process_enum_boot_item(parser: TagValTextParser) -> MenuEnumBootCommand:
        choices: tuple[str, ...] = TagValMenuCommandProcessors._choices_from_msg(parser)
        item: EnumMenuItem = EnumMenuItem(
            id=parser.get_value_as_int(TagValMenuFields.KEY_ID_FIELD.value),
            eeprom_address=parser.get_value_as_int(TagValMenuFields.KEY_EEPROM_FIELD.value, 0),
            name=parser.get_value(TagValMenuFields.KEY_NAME_FIELD.value),
            read_only=parser.get_value_as_int(TagValMenuFields.KEY_READONLY_FIELD.value) != 0,
            visible=parser.get_value_as_int(TagValMenuFields.KEY_VISIBLE_FIELD.value, 1) != 0,
            enum_entries=choices,
        )

        parent_id: int = parser.get_value_as_int(TagValMenuFields.KEY_PARENT_ID_FIELD.value)
        current_val: int = parser.get_value_as_int(TagValMenuFields.KEY_CURRENT_VAL.value)

        return CommandFactory.new_menu_enum_boot_command(parent_id=parent_id, item=item, current_value=current_val)

    @staticmethod
    def _process_boolean_boot_item(parser: TagValTextParser) -> MenuBooleanBootCommand:
        item: BooleanMenuItem = BooleanMenuItem(
            id=parser.get_value_as_int(TagValMenuFields.KEY_ID_FIELD.value),
            eeprom_address=parser.get_value_as_int(TagValMenuFields.KEY_EEPROM_FIELD.value, 0),
            name=parser.get_value(TagValMenuFields.KEY_NAME_FIELD.value),
            read_only=parser.get_value_as_int(TagValMenuFields.KEY_READONLY_FIELD.value) != 0,
            visible=parser.get_value_as_int(TagValMenuFields.KEY_VISIBLE_FIELD.value, 1) != 0,
            naming=BooleanMenuItem.BooleanNaming.from_id(
                parser.get_value_as_int(TagValMenuFields.KEY_BOOLEAN_NAMING.value)
            ),
        )

        parent_id: int = parser.get_value_as_int(TagValMenuFields.KEY_PARENT_ID_FIELD.value)
        current_val: int = parser.get_value_as_int(TagValMenuFields.KEY_CURRENT_VAL.value)

        return CommandFactory.new_menu_boolean_boot_command(
            parent_id=parent_id, item=item, current_value=current_val != 0
        )

    @staticmethod
    def _process_large_num_boot_item(parser: TagValTextParser) -> MenuLargeNumBootCommand:
        item: EditableLargeNumberMenuItem = EditableLargeNumberMenuItem(
            id=parser.get_value_as_int(TagValMenuFields.KEY_ID_FIELD.value),
            eeprom_address=parser.get_value_as_int(TagValMenuFields.KEY_EEPROM_FIELD.value, 0),
            name=parser.get_value(TagValMenuFields.KEY_NAME_FIELD.value),
            read_only=parser.get_value_as_int(TagValMenuFields.KEY_READONLY_FIELD.value) != 0,
            visible=parser.get_value_as_int(TagValMenuFields.KEY_VISIBLE_FIELD.value, 1) != 0,
            decimal_places=parser.get_value_as_int(TagValMenuFields.KEY_FLOAT_DECIMAL_PLACES.value),
            negative_allowed=parser.get_value_as_int(TagValMenuFields.KEY_NEGATIVE_ALLOWED.value, 1) != 0,
            digits_allowed=parser.get_value_as_int(TagValMenuFields.KEY_MAX_LENGTH.value),
        )

        parent_id: int = parser.get_value_as_int(TagValMenuFields.KEY_PARENT_ID_FIELD.value)
        current_val: str = parser.get_value(TagValMenuFields.KEY_CURRENT_VAL.value).replace("[", "").replace("]", "")

        return CommandFactory.new_menu_large_item_boot_command(
            parent_id=parent_id, item=item, current_value=float(current_val)
        )

    @staticmethod
    def _process_item_change(parser: TagValTextParser) -> MenuChangeCommand:
        change_type: MenuChangeCommand.ChangeType = MenuChangeCommand.ChangeType.from_id(
            parser.get_value_as_int(TagValMenuFields.KEY_CHANGE_TYPE.value)
        )

        correlation_str: str = parser.get_value(TagValMenuFields.KEY_CORRELATION_FIELD.value, "")
        # noinspection PyUnresolvedReferences
        correlation: CorrelationId = (
            CorrelationId.from_string(correlation_str) if len(correlation_str) != 0 else CorrelationId.EMPTY_CORRELATION
        )

        if change_type == MenuChangeCommand.ChangeType.DELTA:
            return CommandFactory.new_delta_menu_change_command(
                correlation_id=correlation,
                item=parser.get_value_as_int(TagValMenuFields.KEY_ID_FIELD.value),
                value=parser.get_value_as_int(TagValMenuFields.KEY_CURRENT_VAL.value),
            )
        elif change_type == MenuChangeCommand.ChangeType.ABSOLUTE:
            return CommandFactory.new_absolute_menu_change_command(
                correlation_id=correlation,
                item=parser.get_value_as_int(TagValMenuFields.KEY_ID_FIELD.value),
                value=parser.get_value_as_int(TagValMenuFields.KEY_CURRENT_VAL.value),
            )
        elif change_type == MenuChangeCommand.ChangeType.LIST_STATE_CHANGE:
            # noinspection PyUnresolvedReferences
            list_response: ListResponse = (
                ListResponse.from_string(parser.get_value(TagValMenuFields.KEY_CURRENT_VAL.value)) or ListResponse.EMPTY
            )

            return CommandFactory.new_list_response_menu_change_command(
                correlation_id=correlation,
                item=parser.get_value_as_int(TagValMenuFields.KEY_ID_FIELD.value),
                value=list_response,
            )
        elif change_type == MenuChangeCommand.ChangeType.ABSOLUTE_LIST:
            choices: tuple[str, ...] = TagValMenuCommandProcessors._choices_from_msg(parser)

            return CommandFactory.new_absolute_list_menu_change_command(
                correlation_id=correlation,
                item=parser.get_value_as_int(TagValMenuFields.KEY_ID_FIELD.value),
                values=choices,
            )

    @staticmethod
    def _process_text_boot_item(parser: TagValTextParser) -> MenuTextBootCommand:
        item: EditableTextMenuItem = EditableTextMenuItem(
            id=parser.get_value_as_int(TagValMenuFields.KEY_ID_FIELD.value),
            eeprom_address=parser.get_value_as_int(TagValMenuFields.KEY_EEPROM_FIELD.value, 0),
            name=parser.get_value(TagValMenuFields.KEY_NAME_FIELD.value),
            read_only=parser.get_value_as_int(TagValMenuFields.KEY_READONLY_FIELD.value) != 0,
            visible=parser.get_value_as_int(TagValMenuFields.KEY_VISIBLE_FIELD.value, 1) != 0,
            item_type=EditItemType.from_id(parser.get_value_as_int(TagValMenuFields.KEY_EDIT_TYPE.value)),
            text_length=parser.get_value_as_int(TagValMenuFields.KEY_MAX_LENGTH.value),
        )

        parent_id: int = parser.get_value_as_int(TagValMenuFields.KEY_PARENT_ID_FIELD.value)
        current_val: str = parser.get_value(TagValMenuFields.KEY_CURRENT_VAL.value)

        return CommandFactory.new_menu_text_boot_command(parent_id=parent_id, item=item, current_value=current_val)

    @staticmethod
    def _process_float_boot_item(parser: TagValTextParser) -> MenuFloatBootCommand:
        item: FloatMenuItem = FloatMenuItem(
            id=parser.get_value_as_int(TagValMenuFields.KEY_ID_FIELD.value),
            eeprom_address=parser.get_value_as_int(TagValMenuFields.KEY_EEPROM_FIELD.value, 0),
            name=parser.get_value(TagValMenuFields.KEY_NAME_FIELD.value),
            read_only=parser.get_value_as_int(TagValMenuFields.KEY_READONLY_FIELD.value) != 0,
            visible=parser.get_value_as_int(TagValMenuFields.KEY_VISIBLE_FIELD.value, 1) != 0,
            num_decimal_places=parser.get_value_as_int(TagValMenuFields.KEY_FLOAT_DECIMAL_PLACES.value),
        )

        parent_id: int = parser.get_value_as_int(TagValMenuFields.KEY_PARENT_ID_FIELD.value)
        current_val: str = parser.get_value(TagValMenuFields.KEY_CURRENT_VAL.value)

        return CommandFactory.new_menu_float_boot_command(
            parent_id=parent_id, item=item, current_value=float(current_val)
        )

    @staticmethod
    def _process_action_boot_item(parser: TagValTextParser) -> MenuActionBootCommand:
        item: ActionMenuItem = ActionMenuItem(
            id=parser.get_value_as_int(TagValMenuFields.KEY_ID_FIELD.value),
            eeprom_address=parser.get_value_as_int(TagValMenuFields.KEY_EEPROM_FIELD.value, 0),
            name=parser.get_value(TagValMenuFields.KEY_NAME_FIELD.value),
        )

        parent_id: int = parser.get_value_as_int(TagValMenuFields.KEY_PARENT_ID_FIELD.value)

        return MenuActionBootCommand(sub_menu_id=parent_id, menu_item=item, current_value=False)

    @staticmethod
    def _process_runtime_list_boot_item(parser: TagValTextParser) -> MenuRuntimeListBootCommand:
        item: RuntimeListMenuItem = RuntimeListMenuItem(
            id=parser.get_value_as_int(TagValMenuFields.KEY_ID_FIELD.value),
            eeprom_address=parser.get_value_as_int(TagValMenuFields.KEY_EEPROM_FIELD.value, 0),
            name=parser.get_value(TagValMenuFields.KEY_NAME_FIELD.value),
            read_only=parser.get_value_as_int(TagValMenuFields.KEY_READONLY_FIELD.value) != 0,
            visible=parser.get_value_as_int(TagValMenuFields.KEY_VISIBLE_FIELD.value, 1) != 0,
            initial_rows=parser.get_value_as_int(TagValMenuFields.KEY_NO_OF_CHOICES.value),
        )

        parent_id: int = parser.get_value_as_int(TagValMenuFields.KEY_PARENT_ID_FIELD.value)
        choices: tuple[str, ...] = TagValMenuCommandProcessors._choices_from_msg(parser)

        return CommandFactory.new_runtime_list_boot_command(parent_id=parent_id, item=item, current_value=choices)

    @staticmethod
    def _choices_from_msg(parser: TagValTextParser) -> tuple[str, ...]:
        choices: list[str] = []
        no_of_items: int = parser.get_value_as_int(TagValMenuFields.KEY_NO_OF_CHOICES.value)

        for i in range(0, no_of_items):
            key_name: str = TagValMenuFields.KEY_PREPEND_NAMECHOICE.value + chr(i + ord("A"))
            key_val: str = TagValMenuFields.KEY_PREPEND_CHOICE.value + chr(i + ord("A"))
            key_text: str = parser.get_value(key_name, "")
            val_text: str = parser.get_value(key_val, "")

            if len(key_text) == 0:
                choices.append(val_text)
            else:
                choices.append(f"{key_text}\t{val_text}")

        return tuple(choices)

    @staticmethod
    def _process_runtime_rgb_color_item(parser: TagValTextParser) -> MenuRgb32BootCommand:
        item: Rgb32MenuItem = Rgb32MenuItem(
            id=parser.get_value_as_int(TagValMenuFields.KEY_ID_FIELD.value),
            eeprom_address=parser.get_value_as_int(TagValMenuFields.KEY_EEPROM_FIELD.value, 0),
            name=parser.get_value(TagValMenuFields.KEY_NAME_FIELD.value),
            read_only=parser.get_value_as_int(TagValMenuFields.KEY_READONLY_FIELD.value) != 0,
            visible=parser.get_value_as_int(TagValMenuFields.KEY_VISIBLE_FIELD.value, 1) != 0,
            include_alpha_channel=parser.get_value_as_int(TagValMenuFields.KEY_ALPHA_FIELD.value, 0) != 0,
        )

        parent_id: int = parser.get_value_as_int(TagValMenuFields.KEY_PARENT_ID_FIELD.value)
        current_val: str = parser.get_value(TagValMenuFields.KEY_CURRENT_VAL.value)

        return CommandFactory.new_menu_rgb32_boot_command(
            parent_id=parent_id, item=item, current_value=PortableColor.from_html(current_val)
        )

    @staticmethod
    def _process_runtime_scroll_choice(parser: TagValTextParser) -> MenuScrollChoiceBootCommand:
        item: ScrollChoiceMenuItem = ScrollChoiceMenuItem(
            id=parser.get_value_as_int(TagValMenuFields.KEY_ID_FIELD.value),
            eeprom_address=parser.get_value_as_int(TagValMenuFields.KEY_EEPROM_FIELD.value, 0),
            name=parser.get_value(TagValMenuFields.KEY_NAME_FIELD.value),
            read_only=parser.get_value_as_int(TagValMenuFields.KEY_READONLY_FIELD.value) != 0,
            visible=parser.get_value_as_int(TagValMenuFields.KEY_VISIBLE_FIELD.value, 1) != 0,
            item_width=parser.get_value_as_int(TagValMenuFields.KEY_WIDTH_FIELD.value),
            num_entries=parser.get_value_as_int(TagValMenuFields.KEY_NO_OF_CHOICES.value),
        )

        parent_id: int = parser.get_value_as_int(TagValMenuFields.KEY_PARENT_ID_FIELD.value)
        current_val: str = parser.get_value(TagValMenuFields.KEY_CURRENT_VAL.value)

        return CommandFactory.new_menu_scroll_choice_boot_command(
            parent_id=parent_id, item=item, current_value=CurrentScrollPosition.from_text(current_val)
        )

    @staticmethod
    def _process_acknowledgement(parser: TagValTextParser) -> MenuAcknowledgementCommand:
        correlation_id: CorrelationId = CorrelationId.from_string(
            parser.get_value(TagValMenuFields.KEY_CORRELATION_FIELD.value, "0")
        )

        return CommandFactory.new_acknowledgement_command(
            correlation_id=correlation_id,
            status=AckStatus.from_status_code(parser.get_value_as_int(TagValMenuFields.KEY_ACK_STATUS.value)),
        )

    @staticmethod
    def _process_pairing_request(parser: TagValTextParser) -> MenuPairingCommand:
        return CommandFactory.new_pairing_command(
            name=parser.get_value(TagValMenuFields.KEY_NAME_FIELD.value),
            uuid=uuid.UUID(parser.get_value(TagValMenuFields.KEY_UUID_FIELD.value)),
        )

    @staticmethod
    def _process_dialog_update(parser: TagValTextParser) -> MenuDialogCommand:
        cor: str = parser.get_value(TagValMenuFields.KEY_CORRELATION_FIELD.value, "")
        # noinspection PyUnresolvedReferences
        correlation_id: CorrelationId = (
            CorrelationId.from_string(cor) if len(cor) != 0 else CorrelationId.EMPTY_CORRELATION
        )

        return CommandFactory.new_dialog_command(
            mode=DialogMode.from_string(parser.get_value(TagValMenuFields.KEY_MODE_FIELD.value)),
            header=parser.get_value(TagValMenuFields.KEY_HEADER_FIELD.value, ""),
            message=parser.get_value(TagValMenuFields.KEY_BUFFER_FIELD.value, ""),
            button1=MenuButtonType.from_id(parser.get_value_as_int(TagValMenuFields.KEY_BUTTON1_FIELD.value, 0)),
            button2=MenuButtonType.from_id(parser.get_value_as_int(TagValMenuFields.KEY_BUTTON2_FIELD.value, 0)),
            correlation_id=correlation_id,
        )

    @staticmethod
    def _write_join(buffer: io.StringIO, command: MenuJoinCommand) -> None:
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_NAME_FIELD.value, command.my_name)
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_UUID_FIELD.value, command.app_uuid)
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_VER_FIELD.value, command.api_version)
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_PLATFORM_ID.value, command.platform.key)
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_SERIAL_NO.value, command.serial_number)

    @staticmethod
    def _write_heartbeat(buffer: io.StringIO, command: MenuHeartbeatCommand) -> None:
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.HB_FREQUENCY_FIELD.value, command.heartbeat_interval
        )
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.HB_MODE_FIELD.value, command.mode.value)

    @staticmethod
    def _write_bootstrap(buffer: io.StringIO, command: MenuBootstrapCommand) -> None:
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_BOOT_TYPE_FIELD.value, command.boot_type.name
        )

    @staticmethod
    def _write_analog_boot_item(buffer: io.StringIO, command: MenuAnalogBootCommand) -> None:
        TagValMenuCommandProcessors._write_common_boot_fields(buffer, command)
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_ANALOG_OFFSET_FIELD.value, command.menu_item.offset
        )
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_ANALOG_DIVISOR_FIELD.value, command.menu_item.divisor
        )
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_ANALOG_MAX_FIELD.value, command.menu_item.max_value
        )
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_ANALOG_STEP_FIELD.value, command.menu_item.step
        )
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_ANALOG_UNIT_FIELD.value, command.menu_item.unit_name
        )
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_CURRENT_VAL.value, command.current_value)

    @staticmethod
    def _write_sub_menu_boot_item(buffer: io.StringIO, command: MenuSubBootCommand) -> None:
        TagValMenuCommandProcessors._write_common_boot_fields(buffer, command)
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_CURRENT_VAL.value, 0)

    @staticmethod
    def _write_enum_boot_item(buffer: io.StringIO, command: MenuEnumBootCommand) -> None:
        TagValMenuCommandProcessors._write_common_boot_fields(buffer, command)
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_CURRENT_VAL.value, command.current_value)
        entries: tuple[str, ...] = command.menu_item.enum_entries
        TagValMenuCommandProcessors._append_choices(buffer=buffer, entries=entries)

    @staticmethod
    def _write_boolean_boot_item(buffer: io.StringIO, command: MenuBooleanBootCommand) -> None:
        TagValMenuCommandProcessors._write_common_boot_fields(buffer, command)
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_BOOLEAN_NAMING.value, command.menu_item.naming.value
        )
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_CURRENT_VAL.value, 1 if command.current_value is True else 0
        )

    @staticmethod
    def _write_large_num_boot_item(buffer: io.StringIO, command: MenuLargeNumBootCommand) -> None:
        TagValMenuCommandProcessors._write_common_boot_fields(buffer, command)
        decimal_places = command.menu_item.decimal_places
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_FLOAT_DECIMAL_PLACES.value, decimal_places
        )
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_NEGATIVE_ALLOWED.value, 1 if command.menu_item.negative_allowed else 0
        )
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_MAX_LENGTH.value, command.menu_item.digits_allowed
        )

        # Formatting the current value
        current_val = "{:,.{prec}f}".format(command.current_value, prec=decimal_places).replace(",", "")
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_CURRENT_VAL.value, current_val)

    @staticmethod
    def _write_item_change(buffer: io.StringIO, command: MenuChangeCommand) -> None:
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_CORRELATION_FIELD.value, command.correlation_id
        )
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_ID_FIELD.value, command.menu_item_id)
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_CHANGE_TYPE.value, command.change_type.value
        )
        if command.change_type == MenuChangeCommand.ChangeType.ABSOLUTE_LIST:
            TagValMenuCommandProcessors._append_choices(buffer=buffer, entries=command.value)
        else:
            TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_CURRENT_VAL.value, command.value)

    @staticmethod
    def _write_text_boot_item(buffer: io.StringIO, command: MenuTextBootCommand) -> None:
        TagValMenuCommandProcessors._write_common_boot_fields(buffer, command)
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_MAX_LENGTH.value, command.menu_item.text_length
        )
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_EDIT_TYPE.value, command.menu_item.item_type.message_id
        )
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_CURRENT_VAL.value, command.current_value)

    @staticmethod
    def _write_float_boot_item(buffer: io.StringIO, command: MenuFloatBootCommand) -> None:
        TagValMenuCommandProcessors._write_common_boot_fields(buffer, command)
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_FLOAT_DECIMAL_PLACES.value, command.menu_item.num_decimal_places
        )
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_CURRENT_VAL.value, command.current_value)

    @staticmethod
    def _write_action_boot_item(buffer: io.StringIO, command: MenuActionBootCommand) -> None:
        TagValMenuCommandProcessors._write_common_boot_fields(buffer, command)
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_CURRENT_VAL.value, "")

    @staticmethod
    def _write_runtime_list_boot_item(buffer: io.StringIO, command: MenuRuntimeListBootCommand) -> None:
        TagValMenuCommandProcessors._write_common_boot_fields(buffer, command)
        TagValMenuCommandProcessors._append_choices(buffer=buffer, entries=command.current_value)

    @staticmethod
    def _write_runtime_rgb_color_item(buffer: io.StringIO, command: MenuRgb32BootCommand) -> None:
        TagValMenuCommandProcessors._write_common_boot_fields(buffer, command)
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_ALPHA_FIELD.value, 1 if command.menu_item.include_alpha_channel else 0
        )
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_CURRENT_VAL.value, command.current_value)

    @staticmethod
    def _write_runtime_scroll_choice(buffer: io.StringIO, command: MenuScrollChoiceBootCommand) -> None:
        TagValMenuCommandProcessors._write_common_boot_fields(buffer, command)
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_WIDTH_FIELD.value, command.menu_item.item_width
        )
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_NO_OF_CHOICES.value, command.menu_item.num_entries
        )
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_CURRENT_VAL.value, command.current_value)

    @staticmethod
    def _write_acknowledgement(buffer: io.StringIO, command: MenuAcknowledgementCommand) -> None:
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_CORRELATION_FIELD.value, command.correlation_id
        )
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_ACK_STATUS.value, command.ack_status.status_code
        )

    @staticmethod
    def _write_pairing_request(buffer: io.StringIO, command: MenuPairingCommand) -> None:
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_NAME_FIELD.value, command.name)
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_UUID_FIELD.value, command.uuid)

    @staticmethod
    def _write_dialog_update(buffer: io.StringIO, command: MenuDialogCommand) -> None:
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_MODE_FIELD.value, command.dialog_mode.value
        )
        if command.header is not None:
            TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_HEADER_FIELD.value, command.header)
        if command.buffer is not None:
            TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_BUFFER_FIELD.value, command.buffer)
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_BUTTON1_FIELD.value, command.button1.type_value
        )
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_BUTTON2_FIELD.value, command.button2.type_value
        )
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_CORRELATION_FIELD.value, command.correlation_id
        )

    @staticmethod
    def _write_common_boot_fields(buffer: io.StringIO, command: BootItemMenuCommand):
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_PARENT_ID_FIELD.value, command.sub_menu_id
        )
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_ID_FIELD.value, command.menu_item.id)
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_EEPROM_FIELD.value, command.menu_item.eeprom_address
        )
        TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_NAME_FIELD.value, command.menu_item.name)
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_READONLY_FIELD.value, 1 if command.menu_item.read_only else 0
        )
        TagValMenuCommandProcessors._append_field(
            buffer, TagValMenuFields.KEY_VISIBLE_FIELD.value, 1 if command.menu_item.visible else 0
        )

    @staticmethod
    def _append_choices(buffer: io.StringIO, entries: tuple[str, ...]):
        if entries is None:
            TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_NO_OF_CHOICES.value, 0)
        else:
            TagValMenuCommandProcessors._append_field(buffer, TagValMenuFields.KEY_NO_OF_CHOICES.value, len(entries))
            for i, entry in enumerate(entries):
                TagValMenuCommandProcessors._append_field(
                    buffer, TagValMenuFields.KEY_PREPEND_CHOICE.value + chr(65 + i), entry
                )

    @staticmethod
    def _append_field(buffer: io.StringIO, key: str, value: Any):
        if isinstance(value, str):
            if "|" in value:
                value = value.replace("|", "\\|")
            if "=" in value:
                value = value.replace("=", "\\=")

        buffer.write(f"{key}={value}|")
