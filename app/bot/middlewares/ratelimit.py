from collections.abc import Awaitable, Callable
from typing import Any
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from redis.asyncio import Redis
class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self,redis:Redis,rate_limit:float = 0.3):
        self.redis = redis
        self.rate_limit = rate_limit
    async def __call__(
        self,
        handler:Callable[[TelegramObject, dict[str,Any]], Awaitable[Any]],
        event:TelegramObject,
        data:dict[str,Any],
    ):
        if isinstance(event,Message) and event.from_user:
            user_id = event.from_user.id
            redis_key = f"ratelimit:{user_id}"
            is_allowed = await self.redis.set(
                redis_key, "blocked",px=int(self.rate_limit * 1000), nx=True
            )
        if not is_allowed:
            await event.answer("So fast")
            return
        return await handler(event,data)