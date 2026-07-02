from functools import lru_cache
from service.storage.keys import safe_key
from service.storage.storage_factory import StorageFactory

class StorageService:
    def __init__(self, storage):
        self.storage = storage

    async def save(self, data, filepath):
        await self.storage.save(data, safe_key(filepath))

    async def load(self, filepath):
        return await self.storage.load(safe_key(filepath))

    async def delete(self, filepath):
        await self.storage.delete(safe_key(filepath))

    async def get_public_url(self, filepath) -> str:
        return await self.storage.get_public_url(safe_key(filepath))

    async def get_full_path(self, filepath) -> str:
        return await self.storage.get_full_path(safe_key(filepath))


@lru_cache
def get_storage_service() -> StorageService:
    return StorageService(StorageFactory.get_storage())
