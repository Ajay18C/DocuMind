from fastapi import Depends
from functools import lru_cache
from service.storage.storage_factory import StorageFactory

class StorageService:
    def __init__(self, storage):
        self.storage = storage

    async def save(self, data, filepath):
        await self.storage.save(data, filepath)
    
    async def load(self, filepath):
        return await self.storage.load(filepath)
    
    async def delete(self, filepath):
        await self.storage.delete(filepath)
    
    async def get_public_url(self, filepath) -> str:
        return await self.storage.get_public_url(filepath)

    async def get_full_path(self, filepath) -> str:
        return await self.storage.get_full_path(filepath)


@lru_cache
def get_storage_service(
    storage: StorageFactory = Depends(StorageFactory.get_storage),
) -> StorageService:
    return StorageService(storage)
