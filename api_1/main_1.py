from fastapi import FastAPI
import uvicorn
import joblib
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}/{num_id}")
def read_item(item_id: int,num_id:str ,q: str = None):
    return {"item_id": item_id, "q": q, "num_id": num_id}

@app.post("/adults_model/")
def create_item(adults: dict):
    pipeline=joblib.load('pipeline_total.gz')
    DF=pd.DataFrame([adults])
    prediction=pipeline.predict_proba(DF)
    result=float(prediction[0][1])
    return {"prediction": result}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)