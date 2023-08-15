"""Pytest tests for grapecity."""

from bible_alignments import config, grapecity


class TestReader:
    """Test Reader."""

    cfg = config.Configuration(sourceid="NA27", targetid="LEB", targetlanguage="eng", processid="manual")
    rd = grapecity.Reader(configuration=cfg)

    def test_init(self) -> None:
        """Test initialization."""
        # can you can read a file successfully
        ag = self.rd["41004003.1"]
        assert ag.meta == {"process": "manual"}
        assert len(ag.sourceitems) == 1
        assert ag.sourceitems[0].lemma == "ἀκούω"
        assert ag.targetitems[0].text == "--"

    def test_alignmentsets(self) -> None:
        """Test alignmentsets"""
        pass
