from tcmenu.tagval.protocol.api_platform import ApiPlatform


def test_api_platform_arduino():
    api_platform = ApiPlatform.Platform.ARDUINO

    assert api_platform.key == 0
    assert api_platform.description == "Arduino 8-bit"


def test_api_platform_java():
    api_platform = ApiPlatform.Platform.JAVA_API

    assert api_platform.key == 1
    assert api_platform.description == "Java API"


def test_api_platform_arduino32():
    api_platform = ApiPlatform.Platform.ARDUINO32

    assert api_platform.key == 2
    assert api_platform.description == "Arduino 32-bit"


def test_api_platform_dotnet():
    api_platform = ApiPlatform.Platform.DOTNET_API

    assert api_platform.key == 3
    assert api_platform.description == ".NET API"


def test_api_platform_js():
    api_platform = ApiPlatform.Platform.JAVASCRIPT_API

    assert api_platform.key == 4
    assert api_platform.description == "JS API"


def test_api_platform_python():
    api_platform = ApiPlatform.Platform.PYTHON_API

    assert api_platform.key == 5
    assert api_platform.description == "Python API"
