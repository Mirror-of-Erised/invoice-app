import importlib.util


def test_app_package_is_discoverable():
    # Just verify Python can see the 'app' package
    assert importlib.util.find_spec("app") is not None
