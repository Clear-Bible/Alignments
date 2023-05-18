"""Pytest tests for gctarget."""

from bible_alignments import config, gctarget


class TestReader:
    """Test Reader."""

    def test_init(self) -> None:
        """Test initialization."""
        # can you can read a file successfully
        cfg = config.Configuration(sourceid="NA27", targetid="LEB", targetlanguage="eng", processid="manual")
        rd = gctarget.Reader(configuration=cfg)
        assert rd["41004003001"].text == "--"
        assert rd["41004003001"].transType == ""
        assert rd["41004003001"].isPunc == True
        assert rd["41004003001"].isPrimary == False
