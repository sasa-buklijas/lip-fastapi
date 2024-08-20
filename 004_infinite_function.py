from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

@app.get("/hi/{wait_time}") 
async def greet(wait_time: int):
    await asyncio.sleep(wait_time) 
    return f"async Hello? World? after {wait_time}"

def infinite():
    c = 0
    while True:
        c += 1
        print(f'infinite call {c=}')
        time.sleep(5) 


# APPROACH 1
#
# If I start it like this
# then infinite() will block FastAPI
# FastAPI will not rune
# BLOCKS FastAPI
#
# infinite()


# APPROACH 2
#
# another approach is to run in separate thread
# this will work 
# but now you have one thread for infinite and another tread for FastAPI
# basically you have 2 threads
# and if you need to synchronize FastAPI and infinite, 
# then you have all problems with multi-threading applications
# that by using FastAPI(async) you tyred to avoid
# NOT RECOMMENDED
#
# import threading  # noqa: E402
# thread = threading.Thread(target=infinite, name='my_thread')
# thread.start()


# APPROACH 3
#
# infinite() is not async, but blocking. will block FastAPI
# FastAPI will not rune
# BLOCKS FastAPI
#
#_= asyncio.create_task(infinite(), name='my_task')


# APPROACH 4
#
# make async, but use blocking call (time.sleep()) inside of async infinite_2
# this blocking call will make FastAPI not rune
# it will come to
# INFO:     Started server process [7067]
# INFO:     Waiting for application startup.
# but nevere to 
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# BLOCKS FastAPI
#
async def infinite_2():
    c = 0
    while True:
        c += 1
        print(f'infinite_2 call {c=}')
        time.sleep(5) 
#_ = asyncio.create_task(infinite_2(), name='my_task')


# APPROACH 5
#
# this is correct way to do it
# make it async and do not use blocking calls inside of it
async def infinite_3():
    c = 0
    while True:
        c += 1
        print(f'infinite_3 call {c=}')
        await asyncio.sleep(5) 
_ = asyncio.create_task(infinite_3(), name='my_task')


# CONCLUSION
#
# 1. Best: make everything async
# 2. Worst: use threads (if there are blocking calls)
#           but then you have problems with multi-treads synchronization
