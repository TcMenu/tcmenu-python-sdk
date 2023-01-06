from tcmenu.persist.version_info import VersionInfo


def test_version_info_no_patch():
    check_version_info_newer_same("1.2", "1.2", True)
    check_version_info_newer_same("1.1", "1.2", True)
    check_version_info_newer_same("1.2", "1.1", False)


def test_version_info_same():
    check_version_info_newer_same("1.2.3", "1.2.3", True)


def test_version_info_newer():
    check_version_info_newer_same("1.2.3", "1.3.3", True)
    check_version_info_newer_same("1.2.3", "1.2.4", True)
    check_version_info_newer_same("1.2.2", "10.2.2", True)


def test_version_info_older():
    check_version_info_newer_same("1.2.3", "1.2.2", False)
    check_version_info_newer_same("1.2.3", "1.1.3", False)
    check_version_info_newer_same("10.2.2", "1.2.2", False)


def check_version_info_newer_same(ver_src: str, ver_dst: str, should_be_same: bool):
    info_src: VersionInfo = VersionInfo(ver_src)
    info_dst: VersionInfo = VersionInfo(ver_dst)

    assert info_dst.is_same_or_newer_than(info_src) == should_be_same
