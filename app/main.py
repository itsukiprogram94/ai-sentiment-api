# ライブラリのインポート
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware #CORS対応のミドルウェア(APIとフロントエンドの通信を許可するため)
# 作った型(スキーマ)と予測関数のインポート
from app.schemas import PredictRequest, PredictResponse
from app.services.predictor import predict_sentiment

#アプリ本体
app = FastAPI()

#CORSミドルウェアの設定(セキュリティ上の理由から、どこからでもアクセスを許可するのは避けるべき)
#http://localhost:5173 からこのFastAPIにアクセスしてよいという許可を与える設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#APIを登録する
#テスト用のルート("/")と、予測用のルート("/predict")を定義する
@app.get("/")
def read_root():
    return{"message": "Hello, FasrtAPI!"}

#予測用のルート("/predict")を定義する
@app.post("/predict", response_model=PredictResponse)#レスポンス型の指定
def predict(request: PredictRequest):#リクエスト型の指定
    result = predict_sentiment(request.text)
    return result

