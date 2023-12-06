from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI()

# Set up CORS middleware to allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this list with the actual origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScoringItem(BaseModel):
    Budget: float
    FindingSource: float
    Category: str
    TRL_Start: int
    TRL_End: int

def CategoryHandler(e):
    possibilities = ['Full Chain', 'T&S', 'capture', 'utilization']
    for _, pos in enumerate(possibilities):
        if e == pos:
            print(_)
            return _

with open("model.pkl", 'rb') as f:
    model = pickle.load(f)

@app.post('/')
async def scoring_endpoint(item: ScoringItem):
    data = item.dict()
    data['Category'] = CategoryHandler(data['Category'])
    df = pd.DataFrame([data.values()], columns=data.keys())
    yhat = model.predict(df)

    return {"prediction": int(yhat)}
