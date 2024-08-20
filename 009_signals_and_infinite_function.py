import os
import asyncio
import signal
from contextlib import asynccontextmanager
from fastapi import FastAPI


previous_signal_handler = None
init_shutdown = False
infinite_1_done = False


def signal_handler(signum, frame):
    print(f'{signal.Signals(signum).name=} {signal.strsignal(signum)=}')
    global init_shutdown
    init_shutdown = True

    global previous_signal_handler
    signal.signal(signal.SIGTERM, previous_signal_handler)
    os.kill(os.getpid(), signal.SIGTERM) 


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f'Before yield is shutdown {os.getpid()=}')
    
    signal.signal(signal.SIGINT, signal_handler)    # CRTL+C
    global previous_signal_handler
    previous_signal_handler = signal.signal(signal.SIGTERM, signal_handler)

    _ = asyncio.create_task(infinite_1(), name='my_task')
    print(f'Before yield {_.done()=}')

    yield
    
    # wait for infinite_1 to finish
    global infinite_1_done
    while infinite_1_done is False:
        print('waiting...')
        await asyncio.sleep(0.5)

    print(f'After yield {_.done()=}')
    print('After yield is shutdown')


app = FastAPI(lifespan=lifespan)


@app.get("/hi/{wait_time}") 
async def greet(wait_time: int):
    await asyncio.sleep(wait_time) 
    return f"async Hello? World? after {wait_time}"


async def infinite_1():
    c = 0
    global init_shutdown
    while init_shutdown is False:
        c += 1
        print(f'infinite_1 call {c=}')
        await asyncio.sleep(2)

    global infinite_1_done
    infinite_1_done = True
    # print for final shutdown
    print(f'Shutdown infinite_1 {init_shutdown=}')
