from config.settings import settings
from service.storage.base_storage import BaseStorage


class StorageFactory:
    @staticmethod
    def get_storage() -> BaseStorage:
        if settings.FILE_STORAGE == "local":
            from .local_storage import LocalStorage

            return LocalStorage()
        elif settings.FILE_STORAGE == "r2":
            from .cloudflarier2_storage import Cloudflarier2Storage

            return Cloudflarier2Storage()
        else:
            raise ValueError(f"Unknown storage type: {settings.FILE_STORAGE}")