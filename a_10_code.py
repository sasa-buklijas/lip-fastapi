import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f'Lifetime ON {os.getpid()=}')
    app.state.global_rw = 0

    _ = asyncio.create_task(infinite_1(app.state), name='my_task')
    yield 

app = FastAPI(lifespan=lifespan)

@app.get("/state/") 
async def inc(request: Request):
    return {'rw': request.app.state.global_rw}

async def infinite_1(app_rw_state):
    print('infinite_1 ON')
    while True:
        app_rw_state.global_rw += 1
        print(f'infinite_1 {app_rw_state.global_rw=}')
        await asyncio.sleep(10) 
