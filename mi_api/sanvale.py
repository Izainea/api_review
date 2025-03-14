from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int,q: str = None):
    if item_id%2 == 0:
        return {"item_id": item_id, "q": "ES PAR!", }
    else:
        return {"item_id": item_id, "q": "ES IMPAR!", }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)