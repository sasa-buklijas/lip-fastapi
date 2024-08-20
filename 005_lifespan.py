import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI


# how to do something on_startup and on_shutdowns
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f'Before yield is shutdown {os.getpid()=}')
    yield
    print('After yield is shutdown')


# https://fastapi.tiangolo.com/advanced/events/
app = FastAPI(lifespan=lifespan)

@app.get("/hi/{wait_time}") 
async def greet(wait_time: int):
    await asyncio.sleep(wait_time) 
    return f"async Hello? World? after {wait_time}"
