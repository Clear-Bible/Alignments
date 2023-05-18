"""Pytest tests for gcsource."""

from bible_alignments import config, gcsource


class TestReader:
    """Test Reader."""

    def test_init(self) -> None:
        """Test initialization."""
        # can you can read a file successfully
        cfg = config.Configuration(sourceid="NA27", targetid="LEB", targetlanguage="eng", processid="manual")
        rd = gcsource.Reader(configuration=cfg)
        assert rd["410040030011"].gloss == "listen,"
        assert rd["410040030011"].lemma == "ἀκούω"
