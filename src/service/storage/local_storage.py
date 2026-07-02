from service.storage.base_storage import BaseStorage
import aiofiles
import aiofiles.os
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[3]


class LocalStorage(BaseStorage):
    def __init__(self):
        self.base_path = PROJECT_ROOT / "local_storage"
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    async def save(self, data, filepath):
        full_path = self.base_path / filepath
        await aiofiles.os.makedirs(full_path.parent, exist_ok=True)
        async with aiofiles.open(full_path, 'wb') as f:
            await f.write(data)

    async def load(self, filepath):
        full_path = self.base_path / filepath
        async with aiofiles.open(full_path, 'rb') as f:
            return await f.read()

    async def delete(self, filepath):
        full_path = self.base_path / filepath
        await aiofiles.os.remove(full_path)

    async def get_public_url(self, filepath) -> str:
        return (self.base_path / filepath).as_uri()
    
    async def get_full_path(self, filepath) -> str:
        return str(self.base_path / filepath)
