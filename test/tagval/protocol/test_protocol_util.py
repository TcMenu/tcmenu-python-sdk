import tcmenu
from tcmenu.tagval.protocol.protocol_util import ProtocolUtil
from tcmenu.tagval.protocol.api_platform import ApiPlatform


def test_module_version_code(mocker):
    mocker.patch.object(tcmenu, '__version__', new="3.2.1")
    assert ProtocolUtil.get_module_version_code() == 302


def test_from_key_to_api_platform():
    assert ProtocolUtil.from_key_to_api_platform(5) == ApiPlatform.PYTHON_API
