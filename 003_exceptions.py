from fastapi import FastAPI, HTTPException


app = FastAPI()

@app.get("/t1/") 
async def test_1():
    # will this crash server
        # not it does not 
    _ = 3 / 0
    return 'OK'

@app.get("/t2/") 
async def test_2():
    return 'Hello World from t2'

@app.get("/t3/") 
async def test_3():
    try:
        _ = 3 / 0
    except Exception as e:
        print(e)
        return { "error": str(e) }
    
    return 'From T3'

@app.get("/t4/") 
async def test_4():
    try:
        _ = 3 / 0
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f'"error": {str(e)}')
    
    return 'From T4'

# this is working with no problem 
    # not sure is it useful 
@app.get("/t5/") 
async def test_5():
    try:
        #_ = 3 / 0
        raise HTTPException(status_code=400, detail='ERROR FROM 5')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f'"error": {str(e)}')
    
    return 'From T5'