# AI Sentiment Web App

React + TypeScript のフロントエンドと FastAPI のバックエンドで作成した、シンプルな感情分析Webアプリです。

入力された英文テキストに対して、`positive` / `negative` / `neutral` のいずれかを判定し、スコアとともに画面に表示します。

## 概要

このプロジェクトでは、React frontend と FastAPI backend を連携させています。

開発中は React と FastAPI を別々のサーバーで起動できます。

```text
React frontend: http://localhost:5173
FastAPI backend: http://127.0.0.1:8000
```

また、本番を見据えて、React を `npm run build` で静的ファイルに変換し、FastAPI から配信する一体型構成にも対応しています。

```text
FastAPI: http://127.0.0.1:8000
├── /             -> React画面
├── /assets/...   -> ReactのJS/CSS
├── /api/health   -> ヘルスチェックAPI
└── /api/predict  -> 感情分析API
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
- ローディング状態の表示
- API通信失敗時のエラー表示
- FastAPIによるAPI提供
- Pydanticによるリクエスト・レスポンスの型定義
- CORS設定による開発時のフロントエンド・バックエンド連携
- React build成果物のFastAPI配信
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
│   │   ├── App.tsx
│   │   └── App.css
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
- APIエンドポイントの定義
- React build成果物の配信

定義している主なエンドポイント：

- `GET /api/health`
- `POST /api/predict`
- `GET /{full_path:path}`

`GET /{full_path:path}` では、React build後の `frontend/dist/index.html` を返します。

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
- ローディング状態の管理
- エラー状態の管理
- 判定ラベルに応じた表示切り替え

### `frontend/src/App.css`

画面デザインを定義しています。

主な内容：

- カード型レイアウト
- 入力フォーム
- ボタン
- 結果表示
- エラー表示
- positive / negative / neutral に応じたラベル表示

## 開発時の起動方法

開発時は Backend と Frontend を別々に起動します。

### 1. Backendを起動する

プロジェクト直下で以下を実行します。

```bash
docker compose up --build
```

または、Dockerを使わずに起動する場合：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backendは以下で起動します。

```text
http://127.0.0.1:8000
```

APIドキュメントは以下で確認できます。

```text
http://127.0.0.1:8000/docs
```

### 2. Frontendを起動する

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

## 一体型構成での起動方法

Reactをbuildして、FastAPIから配信する構成です。

### 1. Reactをbuildする

```bash
cd frontend
npm install
npm run build
cd ..
```

成功すると、以下のフォルダが生成されます。

```text
frontend/dist/
```

### 2. FastAPIを起動する

```bash
uvicorn app.main:app --reload
```

またはDockerで起動します。

```bash
docker compose up --build
```

### 3. ブラウザで確認する

以下にアクセスします。

```text
http://127.0.0.1:8000
```

FastAPIからReact画面が配信されます。

## 使い方

1. アプリを起動する
2. テキストを入力する
3. `Analyze` ボタンを押す
4. 判定結果が画面に表示される

入力例：

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

### GET /api/health

ヘルスチェック用エンドポイントです。

レスポンス例：

```json
{
  "message": "Hello, FastAPI"
}
```

### POST /api/predict

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

開発時は Frontend と Backend が別々のオリジンで動きます。

```text
Frontend: http://localhost:5173
Backend:  http://127.0.0.1:8000
```

ポートが異なるため、ブラウザ上では別オリジンとして扱われます。

そのため、FastAPI側で `CORSMiddleware` を使い、React frontend からのアクセスを許可しています。

一体型構成では、React画面とAPIが同じオリジンから提供されます。

```text
http://127.0.0.1:8000
```

そのため、本番想定の一体型構成ではCORS問題は基本的に発生しません。

## 現在の制限

- ルールベースの簡易判定であり、実際の機械学習モデルは使用していません
- 英文テキストのみを想定しています
- Frontendのbuild成果物はGit管理していません
- Dockerfileはまだ完全な一体型buildには対応していません
- 本番環境へのデプロイは未実施です

## 今後の改善案

- 一体型Dockerfileへの更新
- scikit-learnによる機械学習モデルへの置き換え
- 日本語テキストへの対応
- pytestによるBackendテスト追加
- VitestなどによるFrontendテスト追加
- GitHub ActionsによるCI追加
- Cloud Run / Render / Railway などへのデプロイ