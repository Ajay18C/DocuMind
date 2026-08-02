class FixedChunker:
    def __init__(self, chunk_size: int, overlap: int):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        chunks = []
        for start in range(0, len(text), self.chunk_size - self.overlap):
            piece = text[start : start + self.chunk_size]
            if piece.strip():
                chunks.append(piece)
            if start + self.chunk_size >= len(text):
                break
        return chunks
