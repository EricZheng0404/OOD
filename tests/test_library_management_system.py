import pytest

@pytest.fixture
def setup():
    print("Start")
    yield
    print("Close")

def test_1(setup):
    print("Test 1")