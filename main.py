from fastapi import FastAPI, BackgroundTasks, Query, Request
import uvicorn
from implementations.DentalStallParser import DentalStallParser
from implementations.storage.FileStorage import FileStorageInterface
from implementations.notifications.ConsoleNotification import ConsoleNotification
from implementations.notifications.EmailNotification import EmailNotification
from contextlib import asynccontextmanager
import os
from pathlib import Path
from configs.redis import init_redis, close_redis,RedisClient
import json
@asynccontextmanager
async def startup(app: FastAPI):
    os.environ['BASE_DIR'] = str(Path(__file__).parent)
    if not os.path.exists(f"{os.environ.get('BASE_DIR')}/data"):
        os.makedirs(f"{os.environ.get('BASE_DIR')}/data")
    await init_redis(app)
    rc = await RedisClient.get_instance()
    await rc.flushall()
    yield
    await close_redis()
app = FastAPI(lifespan=startup)


@app.get("/scrape-simple")
async def home(background_tasks: BackgroundTasks, pages: int = 1,proxy:str=""):
    dp = DentalStallParser("https://dentalstall.com/shop/page/")
    msg = await dp.parse(pages, proxy,storer=FileStorageInterface("data/parsed_data.json"), notifier=ConsoleNotification(recipients=["abc@abc.com"]), background_tasks=background_tasks)

    return {"message": msg}


@app.get("/scrape-email")
async def home(background_tasks: BackgroundTasks, request: Request, pages: int = 1,proxy:str=""):
    dp = DentalStallParser("https://dentalstall.com/shop/page/")
    res = await request.body()
    msg = await dp.parse(pages, proxy,storer=FileStorageInterface("data/parsed_data.json"), notifier=EmailNotification(recipient_emails=json.loads(res.decode('utf-8'))['recipient_emails']), background_tasks=background_tasks)

    return {"message": msg}
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
