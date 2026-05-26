from pathlib import Path
# ライブラリのインポート
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware #CORS対応のミドルウェア(APIとフロントエンドの通信を許可するため)
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
# 作った型(スキーマ)と予測関数のインポート
from app.schemas import PredictRequest, PredictResponse
from app.services.predictor import predict_sentiment

#アプリ本体
app = FastAPI()
#Reactのビルド成果物が置いてあるディレクトリへのパスを指定
frontend_dist_path = Path("frontend/dist")

#CORSミドルウェアの設定(セキュリティ上の理由から、どこからでもアクセスを許可するのは避けるべき)
#http://localhost:5173 からこのFastAPIにアクセスしてよいという許可を与える設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"message": "Hello, FastAPI"}

#予測用のルート("/api/predict")を定義する
@app.post("/api/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    result = predict_sentiment(request.text)
    return result

#静的ファイルを提供するディレクトリを特定のパスに紐付け
if frontend_dist_path.exists():
    app.mount(
        "/assets",
        StaticFiles(directory=frontend_dist_path / "assets"),
        name="assets",
    )

#GETリクエストで、どんなパスが来ても受け取る
@app.get("/{full_path:path}")
def serve_react_app(full_path: str):
    index_file = frontend_dist_path / "index.html"

    if index_file.exists():
        return FileResponse(index_file)

    return {
        "message": "Frontend build not found. Run `cd frontend && npm run build` first."
    }


#APIを登録する
#テスト用のルート("/")と、予測用のルート("/predict")を定義する
#@app.get("/")
#def read_root():
#    return{"message": "Hello, FasrtAPI!"}



