from enum import Enum


class TagValMenuFields(Enum):
    """
    Field names are used to represent the possible field names that can be sent to a remote menu. These must
    be the same at both sides to be understood. All fields starting with an upper or lower case letter are
    reserved. Letters starting with digits 0 to 9 are not reserved. Fields must be exactly two letters.
    """

    KEY_NAME_FIELD: str = "NM"
    KEY_UUID_FIELD: str = "UU"
    KEY_SERIAL_NO: str = "US"
    KEY_VER_FIELD: str = "VE"
    HB_FREQUENCY_FIELD: str = "HI"
    HB_MODE_FIELD: str = "HR"
    KEY_PLATFORM_ID: str = "PF"
    KEY_BOOT_TYPE_FIELD: str = "BT"
    KEY_ID_FIELD: str = "ID"
    KEY_CORRELATION_FIELD: str = "IC"
    KEY_EEPROM_FIELD: str = "IE"
    KEY_READONLY_FIELD: str = "RO"
    KEY_VISIBLE_FIELD: str = "VI"
    KEY_ALPHA_FIELD: str = "RA"
    KEY_WIDTH_FIELD: str = "WI"
    KEY_PARENT_ID_FIELD: str = "PI"
    KEY_ANALOG_MAX_FIELD: str = "AM"
    KEY_ANALOG_OFFSET_FIELD: str = "AO"
    KEY_ANALOG_STEP_FIELD: str = "AS"
    KEY_ANALOG_DIVISOR_FIELD: str = "AD"
    KEY_ANALOG_UNIT_FIELD: str = "AU"
    KEY_FLOAT_DECIMAL_PLACES: str = "FD"
    KEY_NEGATIVE_ALLOWED: str = "NA"
    KEY_REMOTE_NUM: str = "RN"
    KEY_CURRENT_VAL: str = "VC"
    KEY_BOOLEAN_NAMING: str = "BN"
    KEY_NO_OF_CHOICES: str = "NC"
    KEY_MAX_LENGTH: str = "ML"
    KEY_EDIT_TYPE: str = "EM"
    KEY_PREPEND_CHOICE: str = "C"  # second char from A onwards.
    KEY_PREPEND_NAMECHOICE: str = "c"  # second char from A onwards.
    KEY_CHANGE_TYPE: str = "TC"
    KEY_ACK_STATUS: str = "ST"
    KEY_MODE_FIELD: str = "MO"
    KEY_BUFFER_FIELD: str = "BU"
    KEY_HEADER_FIELD: str = "HF"
    KEY_BUTTON1_FIELD: str = "B1"
    KEY_BUTTON2_FIELD: str = "B2"
