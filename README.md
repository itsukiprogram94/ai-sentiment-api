# AI Sentiment API

FastAPIで作成したシンプルな感情分析APIです。  
入力された英文テキストに対して、positive / negative / neutral のいずれかを返します。

## 使用技術

- Python
- FastAPI
- Pydantic
- Uvicorn
- Docker
- Docker Compose

## 機能

- `GET /` : ヘルスチェック用エンドポイント
- `POST /predict` : 感情分析を行うエンドポイント

## ディレクトリ構成

```text
ai-sentiment-api/
├── app/
│   ├── main.py
│   ├── schemas.py
│   └── services/
│       └── predictor.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 起動方法

### Dockerを使う場合

```bash
docker compose up --build
```

起動後、以下にアクセスします。

```text
http://127.0.0.1:8000/docs
```

### ローカル環境で起動する場合

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API仕様

### POST /predict

リクエスト例：

```json
{
  "text": "This product is excellent"
}
```

レスポンス例：

```json
{
  "text": "This product is excellent",
  "label": "positive",
  "score": 0.9
}
```

## 現在の判定ロジック

現時点では、機械学習モデルではなく、単語リストを使った簡易的なルールベース判定を行っています。

例：

- positive: love, good, great, excellent, happy
- negative: bad, hate, terrible, sad, poor

## 今後の改善案

- scikit-learnによる機械学習モデルへの置き換え
- pytestによるテスト追加
- GitHub ActionsによるCI追加
- Cloud Runなどへのデプロイ
- 日本語テキストへの対応