import pytest


@pytest.mark.describe("Sanity")
class TestSanity:
    @pytest.mark.it("Should pass")
    def test_sanity(self) -> None:
        assert True
