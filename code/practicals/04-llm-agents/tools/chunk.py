"""Chunk filings into overlapping word windows (deterministic)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    doc: str        # source filename
    index: int      # position within the document
    text: str

    @property
    def id(self) -> str:
        return f"{self.doc}#{self.index}"


def chunk_text(text: str, source: str, *, size: int = 60, overlap: int = 15) -> list[Chunk]:
    """Split *text* into ~`size`-word chunks overlapping by `overlap` words."""
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    words = text.split()
    if not words:
        return []
    step = size - overlap
    chunks: list[Chunk] = []
    for start in range(0, len(words), step):
        segment = words[start:start + size]
        if not segment:
            break
        chunks.append(Chunk(source, len(chunks), " ".join(segment)))
        if start + size >= len(words):
            break
    return chunks


def chunk_corpus(docs: dict[str, str], *, size: int = 60, overlap: int = 15) -> list[Chunk]:
    """Chunk a whole ``{filename: text}`` corpus into one flat list."""
    out: list[Chunk] = []
    for name, text in docs.items():
        out.extend(chunk_text(text, name, size=size, overlap=overlap))
    return out
