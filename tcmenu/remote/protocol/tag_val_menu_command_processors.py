import io

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
)
from tcmenu.remote.commands.menu_bootstrap_command import MenuBootstrapCommand
from tcmenu.remote.commands.menu_button_type import MenuButtonType
from tcmenu.remote.commands.menu_change_command import MenuChangeCommand
from tcmenu.remote.commands.menu_command import MenuCommand
from tcmenu.remote.commands.menu_command_type import MenuCommandType
from tcmenu.remote.commands.menu_dialog_command import MenuDialogCommand
from tcmenu.remote.commands.menu_heartbeat_command import MenuHeartbeatCommand
from tcmenu.remote.commands.menu_join_command import MenuJoinCommand
from tcmenu.remote.commands.menu_pairing_command import MenuPairingCommand
from tcmenu.remote.protocol.configurable_protocol_converter import ConfigurableProtocolConverter
from tcmenu.remote.protocol.tag_val_text_parser import TagValTextParser


class TagValMenuCommandProcessors:
    @staticmethod
    def add_handlers_to_protocol(proto: ConfigurableProtocolConverter):
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
    def _process_join(parser: TagValTextParser) -> MenuCommand:
        pass

    @staticmethod
    def _process_heartbeat(parser: TagValTextParser) -> MenuCommand:
        pass

    @staticmethod
    def _process_bootstrap(parser: TagValTextParser) -> MenuCommand:
        pass

    @staticmethod
    def _process_analog_boot_item(parser: TagValTextParser) -> MenuCommand:
        pass

    @staticmethod
    def _process_sub_menu_boot_item(parser: TagValTextParser) -> MenuCommand:
        pass

    @staticmethod
    def _process_enum_boot_item(parser: TagValTextParser) -> MenuCommand:
        pass

    @staticmethod
    def _process_boolean_boot_item(parser: TagValTextParser) -> MenuCommand:
        pass

    @staticmethod
    def _process_large_num_boot_item(parser: TagValTextParser) -> MenuCommand:
        pass

    @staticmethod
    def _process_item_change(parser: TagValTextParser) -> MenuCommand:
        pass

    @staticmethod
    def _process_text_boot_item(parser: TagValTextParser) -> MenuCommand:
        pass

    @staticmethod
    def _process_float_boot_item(parser: TagValTextParser) -> MenuCommand:
        pass

    @staticmethod
    def _process_action_boot_item(parser: TagValTextParser) -> MenuCommand:
        pass

    @staticmethod
    def _process_runtime_list_boot_item(parser: TagValTextParser) -> MenuCommand:
        pass

    @staticmethod
    def _process_runtime_rgb_color_item(parser: TagValTextParser) -> MenuCommand:
        pass

    @staticmethod
    def _process_runtime_scroll_choice(parser: TagValTextParser) -> MenuCommand:
        pass

    @staticmethod
    def _process_acknowledgement(parser: TagValTextParser) -> MenuCommand:
        pass

    @staticmethod
    def _process_pairing_request(parser: TagValTextParser) -> MenuCommand:
        pass

    @staticmethod
    def _process_dialog_update(parser: TagValTextParser) -> MenuCommand:
        pass

    @staticmethod
    def _as_dialog_mode(mode: str) -> DialogMode:
        pass

    @staticmethod
    def _as_button(req: int) -> MenuButtonType:
        pass

    @staticmethod
    def _write_join(buffer: io.StringIO, command: MenuCommand) -> None:
        pass

    @staticmethod
    def _write_heartbeat(buffer: io.StringIO, command: MenuCommand) -> None:
        pass

    @staticmethod
    def _write_bootstrap(buffer: io.StringIO, command: MenuCommand) -> None:
        pass

    @staticmethod
    def _write_analog_boot_item(buffer: io.StringIO, command: MenuCommand) -> None:
        pass

    @staticmethod
    def _write_sub_menu_boot_item(buffer: io.StringIO, command: MenuCommand) -> None:
        pass

    @staticmethod
    def _write_enum_boot_item(buffer: io.StringIO, command: MenuCommand) -> None:
        pass

    @staticmethod
    def _write_boolean_boot_item(buffer: io.StringIO, command: MenuCommand) -> None:
        pass

    @staticmethod
    def _write_large_num_boot_item(buffer: io.StringIO, command: MenuCommand) -> None:
        pass

    @staticmethod
    def _write_item_change(buffer: io.StringIO, command: MenuCommand) -> None:
        pass

    @staticmethod
    def _write_text_boot_item(buffer: io.StringIO, command: MenuCommand) -> None:
        pass

    @staticmethod
    def _write_float_boot_item(buffer: io.StringIO, command: MenuCommand) -> None:
        pass

    @staticmethod
    def _write_action_boot_item(buffer: io.StringIO, command: MenuCommand) -> None:
        pass

    @staticmethod
    def _write_runtime_list_boot_item(buffer: io.StringIO, command: MenuCommand) -> None:
        pass

    @staticmethod
    def _write_runtime_rgb_color_item(buffer: io.StringIO, command: MenuCommand) -> None:
        pass

    @staticmethod
    def _write_runtime_scroll_choice(buffer: io.StringIO, command: MenuCommand) -> None:
        pass

    @staticmethod
    def _write_acknowledgement(buffer: io.StringIO, command: MenuCommand) -> None:
        pass

    @staticmethod
    def _write_pairing_request(buffer: io.StringIO, command: MenuCommand) -> None:
        pass

    @staticmethod
    def _write_dialog_update(buffer: io.StringIO, command: MenuCommand) -> None:
        pass
