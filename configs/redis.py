import aioredis
from fastapi import FastAPI
import os
from typing import Optional

class RedisClient:
    _instance: Optional[aioredis.Redis] = None

    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
            cls._instance = await aioredis.from_url(redis_url, decode_responses=True)
        print("REDIS connected")
        return cls._instance

    @classmethod
    async def close(cls):
        if cls._instance:
            await cls._instance.close()


async def init_redis(app: FastAPI):
    app.state.redis = await RedisClient.get_instance()

async def close_redis():
    await RedisClient.close()
    print("REDIS disconnected")