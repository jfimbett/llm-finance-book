from tools.chunk import chunk_text, chunk_corpus
from tools._common import load_corpus


def test_overlap_and_coverage():
    text = " ".join(f"w{i}" for i in range(100))
    chunks = chunk_text(text, "doc", size=30, overlap=10)
    # every word is covered
    covered = set()
    for c in chunks:
        covered.update(c.text.split())
    assert covered == set(text.split())
    # consecutive chunks share `overlap` words
    first = chunks[0].text.split()
    second = chunks[1].text.split()
    assert first[-10:] == second[:10]


def test_ids_are_unique_and_sequential():
    chunks = chunk_corpus(load_corpus(), size=40, overlap=10)
    assert len(chunks) > 0
    assert len({c.id for c in chunks}) == len(chunks)


def test_overlap_must_be_smaller_than_size():
    import pytest
    with pytest.raises(ValueError):
        chunk_text("a b c", "d", size=10, overlap=10)
