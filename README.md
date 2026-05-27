# AI Sentiment Web App

React + TypeScript のフロントエンドと FastAPI のバックエンドで作成した、シンプルな感情分析Webアプリです。

入力された英文テキストに対して、`positive` / `negative` / `neutral` のいずれかを判定し、スコアとともに画面に表示します。

## 概要

このプロジェクトは、React frontend を build し、その build 成果物を FastAPI backend から配信する一体型構成です。

```text
User
↓
FastAPI container
├── /             -> React画面
├── /assets/...   -> ReactのJS/CSS
├── /api/health   -> ヘルスチェックAPI
└── /api/predict  -> 感情分析API
```

Docker build の中で以下を行います。

```text
1. Node.js環境で React frontend を build
2. Python環境で FastAPI backend を用意
3. build済みの frontend/dist を FastAPIコンテナへコピー
4. 1つのコンテナで画面とAPIを配信
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
- 判定ラベルに応じたUI表示切り替え
- Pydanticによるリクエスト・レスポンスの型定義
- React build成果物のFastAPI配信
- multi-stage Docker build による一体型コンテナ作成

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
│   ├── package-lock.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## アプリケーション構成

### `app/main.py`

FastAPIアプリケーションのエントリーポイントです。

主な役割：

- FastAPIアプリの作成
- APIエンドポイントの定義
- React build成果物の配信

定義している主なエンドポイント：

- `GET /api/health`
- `POST /api/predict`
- `GET /`
- `GET /{full_path:path}`

`GET /` および `GET /{full_path:path}` では、React build後の `frontend/dist/index.html` を返します。

### `app/schemas.py`

APIの入力・出力データ構造を定義しています。

- `PredictRequest`
- `PredictResponse`

### `app/services/predictor.py`

感情分析ロジックを定義しています。

現時点では、以下のような単語リストを使って判定しています。

- positive: `love`, `good`, `great`, `excellent`, `happy`
- negative: `bad`, `hate`, `terrible`, `sad`, `poor`

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

## 起動方法

### Dockerで起動する

プロジェクト直下で以下を実行します。

```bash
docker compose up --build
```

起動後、以下にアクセスします。

```text
http://127.0.0.1:8000
```

FastAPIがReact画面を配信し、同じサーバー上でAPIも提供します。

APIドキュメントは以下で確認できます。

```text
http://127.0.0.1:8000/docs
```

ヘルスチェックAPIは以下です。

```text
http://127.0.0.1:8000/api/health
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

## FrontendとAPIの通信

React側では、APIを相対パスで呼び出しています。

```ts
fetch("/api/predict", ...)
```

一体型構成では、React画面とAPIが同じオリジンから提供されます。

```text
http://127.0.0.1:8000
```

そのため、本番想定の一体型構成ではCORS問題は基本的に発生しません。

## Docker構成

このプロジェクトでは、multi-stage build を使用しています。

### 1. Frontend build stage

Node.js環境でReactをbuildします。

```text
frontend/src
↓
npm run build
↓
frontend/dist
```

### 2. Backend runtime stage

Python環境でFastAPIを起動します。

Frontend build stageで生成した `frontend/dist` をFastAPIコンテナへコピーし、FastAPIから静的ファイルとして配信します。

最終的なコンテナには以下が含まれます。

```text
/app
├── app/
│   ├── main.py
│   ├── schemas.py
│   └── services/
└── frontend/
    └── dist/
        ├── index.html
        └── assets/
```

## 開発時にFrontendとBackendを分けて起動する場合

開発中にReactのHot Reloadを使いたい場合は、FrontendとBackendを別々に起動できます。

### Backend

```bash
uvicorn app.main:app --reload
```

または：

```bash
docker compose up --build
```

Backendは以下で起動します。

```text
http://127.0.0.1:8000
```

### Frontend

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

この開発時構成では、FrontendとBackendが別オリジンになるため、FastAPI側のCORS設定が必要になります。

## 注意事項

### `npm run dev` と `npm run build` の違い

`npm run dev` は開発用サーバーを起動するコマンドです。

```text
http://localhost:5173
```

でReactアプリを確認できます。

一方、`npm run build` は本番用の静的ファイルを生成するコマンドです。

```text
frontend/dist/
```

が生成されます。

このプロジェクトのDockerfileでは、Docker build中に `npm run build` を実行し、生成された `frontend/dist` をFastAPIコンテナへコピーします。

## 現在の制限

- ルールベースの簡易判定であり、実際の機械学習モデルは使用していません
- 英文テキストのみを想定しています
- Frontendのbuild成果物 `frontend/dist/` はGit管理していません
- 本番環境へのデプロイは未実施です

## 今後の改善案

- scikit-learnによる機械学習モデルへの置き換え
- 日本語テキストへの対応
- pytestによるBackendテスト追加
- VitestなどによるFrontendテスト追加
- GitHub ActionsによるCI追加
- Cloud Run / Render / Railway などへのデプロイ