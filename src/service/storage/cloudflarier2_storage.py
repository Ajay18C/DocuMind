import aioboto3
from botocore.config import Config
from botocore.exceptions import ClientError

from config.settings import settings

from .base_storage import BaseStorage
from .exceptions import StorageNotFound


class Cloudflarier2Storage(BaseStorage):
    def __init__(self):
        self._bucket = settings.R2_CONFIG.bucket
        self._session = aioboto3.Session()
        self._client_kwargs = dict(
            service_name="s3",
            endpoint_url=f"https://{settings.R2_CONFIG.account_id}.r2.cloudflarestorage.com",
            aws_access_key_id=settings.R2_CONFIG.access_key,
            aws_secret_access_key=settings.R2_CONFIG.secret_key,
            region_name="auto",
            config=Config(signature_version="s3v4"),
        )

    def _client(self):
        return self._session.client(**self._client_kwargs)

    async def save(self, data, filepath: str, content_type: str | None = None):
        extra = {"ContentType": content_type} if content_type else {}
        async with self._client() as client:
            await client.put_object(
                Bucket=self._bucket, Key=filepath, Body=data, **extra
            )

    async def load(self, filepath: str) -> bytes:
        async with self._client() as client:
            try:
                obj = await client.get_object(Bucket=self._bucket, Key=filepath)
                return await obj["Body"].read()
            except ClientError as e:
                if e.response["Error"]["Code"] in ("NoSuchKey", "404"):
                    raise StorageNotFound(filepath) from e
                raise

    async def delete(self, filepath: str):
        async with self._client() as client:
            await client.delete_object(Bucket=self._bucket, Key=filepath)

    async def exists(self, filepath: str) -> bool:
        async with self._client() as client:
            try:
                await client.head_object(Bucket=self._bucket, Key=filepath)
                return True
            except ClientError as e:
                if e.response["Error"]["Code"] in ("404", "NoSuchKey"):
                    return False
                raise

    async def get_public_url(self, filepath: str, expires_in: int = 3600) -> str:
        async with self._client() as client:
            return await client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self._bucket, "Key": filepath},
                ExpiresIn=expires_in,
            )
    
    async def get_full_path(self, filepath: str) -> str:
        return f"https://{self._bucket}.{settings.R2_CONFIG.account_id}.r2.cloudflarestorage.com/{filepath}"
