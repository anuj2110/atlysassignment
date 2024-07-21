from fastapi import FastAPI,BackgroundTasks
import uvicorn
from implementations.DentalStallParser import DentalStallParser
from implementations.storage.FileStorage import FileStorageInterface
from implementations.notifications.ConsoleNotification import ConsoleNotification
from contextlib import asynccontextmanager
import os
from pathlib import Path
@asynccontextmanager
async def startup(app: FastAPI):
    os.environ['BASE_DIR'] = str(Path(__file__).parent)
    yield
app = FastAPI(lifespan=startup)



@app.get("/")
async def home(background_tasks:BackgroundTasks,pages:int=1,proxy=''):
    
    dp = DentalStallParser("https://dentalstall.com/shop/page/")
    await dp.parse(pages,storer=FileStorageInterface("data/parsed_data.json"),notifier=ConsoleNotification(recipients=["abc@abc.com"]),background_tasks=background_tasks)

    return {"message": "running awesome"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
