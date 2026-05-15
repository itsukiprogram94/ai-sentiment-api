from fastapi import FastAPI
from app.schemas import PredictRequest, PredictResponse
from app.services.predictor import predict_sentiment

app = FastAPI()



@app.get("/")
def read_root():
    return{"message": "Hello, FasrtAPI!"}

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    result = predict_sentiment(request.text)
    return result

