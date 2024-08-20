import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request


# some ideas from:
# https://stackoverflow.com/questions/76322463/how-to-initialise-a-global-object-or-variable-and-reuse-it-in-every-fastapi-endp


# how to do something on_startup and on_shutdowns
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f'Before yield is shutdown {os.getpid()=}')
    # read-write global variable access per-request
    app.state.global_rw = 0

    _ = asyncio.create_task(infinite_1(app.state), name='my_task')
    print(f'Before yield {_.done()=}')

    # this is just read only global variable access per-request
    yield {'global_ro': 0}
    print(f'After yield {_.done()=}')
    print('After yield is shutdown')


# https://fastapi.tiangolo.com/advanced/events/
app = FastAPI(lifespan=lifespan)


# depreciated, IT IS NOT HAPPENING
@app.on_event("startup")
async def startup_event():
    print('@app.on_event("startup")')


@app.get("/reset/") 
async def inc(request: Request):
    # only local update
    request.state.global_ro = request.state.global_ro + 5
    # global update 
    old_rw = request.app.state.global_rw
    request.app.state.global_rw = 0
    return {'old_rw': old_rw, 'current_rw': request.app.state.global_rw}


async def infinite_1(app_rw_state):
    # ao that whole FastAPI can start first 
    #await asyncio.sleep(1)
    c = 0
    while True:
        c += 1
        app_rw_state.global_rw += 1
        print(f'infinite_1 call {c=} {app_rw_state.global_rw=}')
        await asyncio.sleep(5) 
# moved in lifespan
#_ = asyncio.create_task(infinite_1(), name='my_task')
