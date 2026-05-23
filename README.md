# AI Sentiment API

React + TypeScript のフロントエンドと FastAPI のバックエンドで作成した、シンプルな感情分析Webアプリです。

入力された英文テキストに対して、`positive` / `negative` / `neutral` のいずれかを判定し、スコアとともに画面に表示します。

## 概要

このプロジェクトでは、以下の流れでフロントエンドとバックエンドを連携しています。

```text
React frontend
↓ fetch
FastAPI backend
↓
sentiment prediction
↓
JSON response
↓
Reactで結果表示
```

現時点では、機械学習モデルではなく、単語リストを用いたルールベースの簡易判定を行っています。

## 使用技術

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn
- Docker
- Docker Compose

### Frontend

- React
- TypeScript
- Vite
- Fetch API

## 主な機能

- テキスト入力フォーム
- 感情分析APIの呼び出し
- 判定結果の画面表示
- FastAPIによるAPI提供
- Pydanticによるリクエスト・レスポンスの型定義
- CORS設定によるフロントエンド・バックエンド連携
- Dockerによるバックエンド実行環境の再現

## ディレクトリ構成

```text
ai-sentiment-api/
├── app/
│   ├── main.py
│   ├── schemas.py
│   └── services/
│       └── predictor.py
├── frontend/
│   ├── src/
│   │   └── App.tsx
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Backend構成

### `app/main.py`

FastAPIアプリケーションのエントリーポイントです。

主な役割：

- FastAPIアプリの作成
- CORS設定
- `GET /` の定義
- `POST /predict` の定義

### `app/schemas.py`

APIの入力・出力データ構造を定義しています。

- `PredictRequest`
- `PredictResponse`

### `app/services/predictor.py`

感情分析ロジックを定義しています。

現時点では、以下のような単語リストを使って判定しています。

- positive: `love`, `good`, `great`, `excellent`, `happy`
- negative: `bad`, `hate`, `terrible`, `sad`, `poor`

## Frontend構成

### `frontend/src/App.tsx`

React + TypeScriptで作成した画面です。

主な役割：

- 入力テキストの状態管理
- Analyzeボタンの処理
- `fetch` による FastAPI へのPOSTリクエスト
- APIレスポンスの画面表示

## 起動方法

## 1. Backendを起動する

プロジェクト直下で以下を実行します。

```bash
docker compose up --build
```

Backendは以下で起動します。

```text
http://127.0.0.1:8000
```

APIドキュメントは以下で確認できます。

```text
http://127.0.0.1:8000/docs
```

### Dockerを使わずに起動する場合

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 2. Frontendを起動する

別ターミナルで以下を実行します。

```bash
cd frontend
npm install
npm run dev
```

Frontendは以下で起動します。

```text
http://localhost:5173
```

## 使い方

1. Backendを起動する
2. Frontendを起動する
3. `http://localhost:5173` にアクセスする
4. テキストを入力する
5. `Analyze` ボタンを押す
6. 判定結果が画面に表示される

例：

```text
This product is excellent
```

出力例：

```text
Text: This product is excellent
Label: positive
Score: 0.9
```

## API仕様

### GET /

ヘルスチェック用エンドポイントです。

レスポンス例：

```json
{
  "message": "Hello, FastAPI"
}
```

### POST /predict

感情分析を行うエンドポイントです。

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

## CORSについて

Frontendは以下で動作します。

```text
http://localhost:5173
```

Backendは以下で動作します。

```text
http://127.0.0.1:8000
```

ポートが異なるため、ブラウザ上では別オリジンとして扱われます。

そのため、FastAPI側で `CORSMiddleware` を使い、React frontend からのアクセスを許可しています。

## 現在の制限

- ルールベースの簡易判定であり、実際の機械学習モデルは使用していません
- 英文テキストのみを想定しています
- エラー処理は最小限です
- Frontendは開発用サーバーで動作しています
- BackendのみDocker化しており、FrontendはまだDocker化していません

## 今後の改善案

- scikit-learnによる機械学習モデルへの置き換え
- 日本語テキストへの対応
- React側のエラー処理追加
- UIデザインの改善
- pytestによるBackendテスト追加
- VitestなどによるFrontendテスト追加
- GitHub ActionsによるCI追加
- FrontendのDocker化
- Cloud Run / Render / Railway などへのデプロイ