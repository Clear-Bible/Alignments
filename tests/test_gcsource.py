"""Pytest tests for gcsource."""

from bible_alignments import gcsource


class TestReader:
    """Test Reader."""

    def test_init(self) -> None:
        """Test initialization."""
        # can you can read a file successfully
        rd = gcsource.Reader(sourceid="NA27", targetid="LEB")
        assert rd["410040030011"].gloss == "listen,"
        assert rd["410040030011"].lemma == "ἀκούω"
