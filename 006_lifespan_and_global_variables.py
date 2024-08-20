
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request


# how to do something on_startup and on_shutdowns
@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Before yield is shutdown')
    # read-write lifetime variable access per-request
    app.state.lifetime_rw = 0
    # this is just read only lifetime variable access per-request
    yield {'lifetime_read_only': 5}   
    print('After yield is shutdown')


# https://fastapi.tiangolo.com/advanced/events/
app = FastAPI(lifespan=lifespan)


@app.get("/inc/") 
async def inc(request: Request):
    # only local update, for this request
    request.state.lifetime_read_only = request.state.lifetime_read_only + 5
    print(f'{request.state.lifetime_read_only=}')
    print(f'{type(request.state.lifetime_read_only)=} in path function.')
    # lifetime update 
    app.state.lifetime_rw += 1

    # this is sending int int
    #wait f_1(request.state.lifetime_read_only, request.app.state.lifetime_rw)

    # this will update it, If I send state then they have access
    # this is sending int, rw=<starlette.datastructures.State object at 0x10ca83080>
    # same functionality as above, but I think it is easier to read when request.app.state is send
    await f_1(request.state.lifetime_read_only, request.app.state)
    return {'lifetime_read_only': request.state.lifetime_read_only, 'times_called': app.state.lifetime_rw}


async def f_1(ro, rw):
    # this is ibtresting here type(ro) is request.state.lifetime_read_only
    # but it is int in async def inc(request: Request):
    print(f'f_1 {ro=} {type(ro)=}')
    print(f'f_1 {rw=} {type(rw)=}')
    # this will not work, it is not possible to update
    # request.state.lifetime_read_only
    ro += 5

    # this is WORKING when we send app.state
    rw.lifetime_rw += 1
    # it is working also, if I send variable directly
    # for when: await f_1(request.state.lifetime_read_only, request.app.state.lifetime_rw)
    #rw += 1

    # do not know what is request
    #print(f'f_1 {request.state.lifetime_read_only=}')
