import os
import asyncio
import signal
from contextlib import asynccontextmanager
from fastapi import FastAPI


# just print what signal receives
def signal_handler(signum, frame):
    print(f'{signal.Signals(signum).name=} {signal.strsignal(signum)=}')
    #exit(0) # not correct way
    #os.kill(os.getpid(), signal.SIGTERM)       # recursion, if not removed first 
    #os.kill(os.getpid(), signal.SIGKILL)     # SIGKILL IT IMIDITLY, no nice shutdown

    # Reset the signal handler to the default behavior
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    os.kill(os.getpid(), signal.SIGTERM) 


# how to do something on_startup and on_shutdowns
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f'Before yield is shutdown {os.getpid()=}')
    #signal.signal(signal.SIGINT, signal_handler)
    #signal.signal(signal.SIGTERM, signal_handler)
    yield
    print('After yield is shutdown')


# https://fastapi.tiangolo.com/advanced/events/
app = FastAPI(lifespan=lifespan)



# start FastAPI
# do curl http://localhost:8000/hi/15
# and CTRL+C or kill -SIGTERM pid
# it will wait for current connection to finish 
#
# even if we do additional 
# curl http://localhost:8000/hi/15
# curl: (7) Failed to connect to localhost port 8000: Connection refused
# it will not work because FastAPI is in shutdown fase
@app.get("/hi/{wait_time}") 
async def greet(wait_time: int):
    await asyncio.sleep(wait_time) 
    return f"async Hello? World? after {wait_time}"
