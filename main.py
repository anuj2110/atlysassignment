from fastapi import FastAPI, BackgroundTasks, Query, Request
import uvicorn
from implementations.DentalStallParser import DentalStallParser
from implementations.storage.FileStorage import FileStorageInterface
from implementations.notifications.ConsoleNotification import ConsoleNotification
from implementations.notifications.EmailNotification import EmailNotification
from contextlib import asynccontextmanager
import os
from pathlib import Path
from configs.redis import init_redis, close_redis


@asynccontextmanager
async def startup(app: FastAPI):
    os.environ['BASE_DIR'] = str(Path(__file__).parent)
    await init_redis(app)
    yield
    await close_redis()
app = FastAPI(lifespan=startup)


@app.get("/scrape-simple")
async def home(background_tasks: BackgroundTasks, pages: int = 1):
    dp = DentalStallParser("https://dentalstall.com/shop/page/")
    await dp.parse(pages, storer=FileStorageInterface("parsed_data.json"), notifier=ConsoleNotification(recipients=["abc@abc.com"]), background_tasks=background_tasks)

    return {"message": "running awesome"}


@app.get("/scrape-email")
async def home(background_tasks: BackgroundTasks, request: Request, pages: int = 1):
    dp = DentalStallParser("https://dentalstall.com/shop/page/")
    print(request.body())
    await dp.parse(pages, storer=FileStorageInterface("parsed_data.json"), notifier=EmailNotification(recipient_emails=["atrehan789@gmail.com"]), background_tasks=background_tasks)

    return {"message": "running awesome"}
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
