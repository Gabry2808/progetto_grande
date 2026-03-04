import arcade
import pytest


@pytest.fixture(scope="session")
def window():
    window = arcade.Window(800, 600)
    yield window
    window.close()
