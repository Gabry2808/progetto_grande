import arcade
import pytest
from collections.abc import Generator


@pytest.fixture(scope="session")
def window() -> Generator[arcade.Window, None, None]:
    window = arcade.Window(800, 600)
    yield window
    window.close()
