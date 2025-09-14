def test_imports():
    import importlib
    m = importlib.import_module("app")
    assert m is not None
