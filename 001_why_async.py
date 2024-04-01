from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

@app.get("/hi/{wait_time}") 
async def greet(wait_time: int):
    await asyncio.sleep(wait_time) 
    return f"async Hello? World? after {wait_time}"

# with /bhi/ idea is to demonstrate blocking in FastAPI
# eg. call /bhi/7 and after /bhi/1, and /bhi1 will be done after /bhi/7
# but this is not happening because FastAPI is running UVicorn can still handle multiple connections concurrently.
@app.get("/bhi/{wait_time}") 
def blocking_greet(wait_time: int):
    time.sleep(wait_time) 
    return f"blocking Hello? World? after {wait_time}"
# check https://fastapi.tiangolo.com/async/#very-technical-details

# this is interesting 
# all async path functions are running in async loop
# because this one is blocking, now whole async loop is blocked 
# but blocking_greet is run in FastAPI thread pool, and that is why it is not blocking
# but if it is called with more workers then it will not block 
# uvicorn 001_why_async:app --workers 2
# explanation check https://fastapi.tiangolo.com/async/#very-technical-details
@app.get("/abhi/{wait_time}") 
async def async_blocking_greet(wait_time: int):
    time.sleep(wait_time) 
    return f"blocking Hello? World? after {wait_time}"

# check 002_why_async_in_flask.py for blocking example
