from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class BaseRepository[T]:
    def __init__(self, model: type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: int) -> T | None:
        return await self.session.get(self.model, id)

    async def list(self) -> list[T]:
        return list((await self.session.scalars(select(self.model))).all())

    async def add(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, id: int) -> None:
        if obj := await self.get(id):
            await self.session.delete(obj)
            await self.session.commit()
    
    async def update(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    
    async def add_many(self, objs: Sequence[T]) -> None:
        self.session.add_all(objs)
        await self.session.commit()

    async def update_many(self, objs: Sequence[T]) -> None:
        self.session.add_all(objs)
        await self.session.commit()
