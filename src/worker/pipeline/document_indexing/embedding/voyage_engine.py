from aiohttp import ClientSession

from model.document_chunk_model import EMBEDDING_DIM

VOYAGE_EMBEDDINGS_URL = "https://api.voyageai.com/v1/embeddings"
EMBEDDING_MODEL = "voyage-4-lite"


class EmbeddingRequestError(Exception):
    pass


class VoyageEmbeddingEngine:
    def __init__(self, api_key: str):
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.session: ClientSession | None = None

    async def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        payload = {
            "input": texts,
            "model": EMBEDDING_MODEL,
            "input_type": "document",
            "output_dimension": EMBEDDING_DIM,
        }
        if self.session is None or self.session.closed:
            self.session = ClientSession()
        async with self.session.post(
            VOYAGE_EMBEDDINGS_URL, json=payload, headers=self.headers
        ) as response:
            if response.status != 200:
                raise EmbeddingRequestError(
                    f"{response.status}: {await response.text()}"
                )
            body = await response.json()
        items = sorted(body["data"], key=lambda item: item["index"])
        return [item["embedding"] for item in items]
