
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request


# how to do something on_startup and on_shutdowns
@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Before yield is shutdown')
    # read-write global variable access per-request
    app.state.global_rw = 0
    # this is just read only global variable access per-request
    yield {'global_read_only': 0}   
    print('After yield is shutdown')


# https://fastapi.tiangolo.com/advanced/events/
app = FastAPI(lifespan=lifespan)


@app.get("/inc/") 
async def inc(request: Request):
    # only local update
    request.state.global_read_only = request.state.global_read_only + 5
    # global update 
    request.app.state.global_rw += 1
    # global did not get updated
    # this is sending int int
    #await f_1(request.state.global_read_only, request.app.state.global_rw)
    # this will update it, If I send state then they have access
    # this is sending int, rw=<starlette.datastructures.State object at 0x10ca83080>
    await f_1(request.state.global_read_only, request.app.state)
    return {'times_called': request.app.state.global_rw, 'global_read_only': request.state.global_read_only}


async def f_1(ro, rw):
    print(f'f_1 {ro=} {type(ro)=}')
    print(f'f_1 {rw=} {type(rw)=}')
    # this will not work 
    #rw += 5

    # this is WORKING when we send request.app.state
    rw.global_rw += 5

    # do not know what is request
    #print(f'f_1 {request.state.global_read_only=}')
