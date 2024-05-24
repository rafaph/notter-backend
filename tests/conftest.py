import os

import pytest

os.environ["LOG_LEVEL"] = "ERROR"


@pytest.fixture()
def anyio_backend() -> tuple[str, dict[str, bool]]:
    return ("asyncio", {"use_uvloop": True})
