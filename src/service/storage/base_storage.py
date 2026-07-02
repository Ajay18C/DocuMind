from abc import ABC, abstractmethod

class BaseStorage(ABC):
    @abstractmethod
    async def save(self, data, filepath):
        pass

    @abstractmethod
    async def load(self, filepath):
        pass

    @abstractmethod
    async def delete(self, filepath):
        pass

    @abstractmethod
    async def get_public_url(self, filepath) -> str:
        pass

    @abstractmethod
    async def get_full_path(self, filepath) -> str:
        pass

    async def exists(self, filepath) -> bool:
        try:
            await self.load(filepath)
            return True
        except FileNotFoundError:
            return False
