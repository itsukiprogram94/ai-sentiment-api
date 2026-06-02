# AI Sentiment Web App

React + TypeScript のフロントエンドと FastAPI のバックエンドで作成した、シンプルな感情分析Webアプリです。

入力された英文テキストに対して、`positive` / `negative` / `neutral` のいずれかを判定し、スコアとともに画面に表示します。

## Demo

Cloud Runで公開しています。

```text
https://ai-sentiment-web-app-909882126486.asia-northeast1.run.app/
```

## Screenshot

![AI Sentiment Web App screenshot](docs/images/app-screenshot.png)

## Overview

このプロジェクトは、React frontend を build し、その build 成果物を FastAPI backend から配信する一体型構成です。

```text
User
↓
Cloud Run
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

現在は、scikit-learnで学習した感情分析モデルを用いて、入力文を `positive` / `negative` / `neutral` に分類しています。

学習データは `data/sentiment_samples.csv` に配置し、`scripts/train_model.py` を実行することでモデルを再学習できます。

## Tech Stack

### Backend

* Python
* FastAPI
* Pydantic
* Uvicorn
* scikit-learn
* pandas
* joblib
* pytest

### Frontend

* React
* TypeScript
* Vite
* Vitest
* React Testing Library
* Fetch API

### Infrastructure / DevOps

* Docker
* Docker Compose
* Cloud Run
* GitHub Actions
* Workload Identity Federation

## Features

* テキスト入力フォーム
* サンプル入力ボタン
* 感情分析APIの呼び出し
* 判定結果の画面表示
* ローディング状態の表示
* API通信失敗時のエラー表示
* 判定ラベルに応じたUI表示切り替え
* Pydanticによるリクエスト・レスポンスの型定義
* scikit-learnによる感情分析モデルの推論
* joblibによる学習済みモデルの保存・読み込み
* CSVデータを用いたモデル再学習
* train/test splitによる簡易的なモデル評価
* pytestによるBackendテスト
* Vitest / React Testing LibraryによるFrontendテスト
* GitHub Actionsによる自動テスト
* GitHub ActionsによるCloud Run自動デプロイ
* React build成果物のFastAPI配信
* multi-stage Docker build による一体型コンテナ作成
* Cloud Runへのデプロイ

## Directory Structure

```text
ai-sentiment-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   ├── models/
│   │   └── sentiment_model.joblib
│   └── services/
│       ├── __init__.py
│       └── predictor.py
├── data/
│   └── sentiment_samples.csv
├── scripts/
│   └── train_model.py
├── tests/
│   ├── test_api.py
│   └── test_predictor.py
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   ├── App.test.tsx
│   │   └── test/
│   │       └── setup.ts
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── docs/
│   └── images/
│       └── app-screenshot.png
├── .github/
│   └── workflows/
│       ├── backend-test.yml
│       └── deploy-cloud-run.yml
├── requirements.txt
├── pytest.ini
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Application Structure

### `app/main.py`

FastAPIアプリケーションのエントリーポイントです。

主な役割：

* FastAPIアプリの作成
* APIエンドポイントの定義
* React build成果物の配信

定義している主なエンドポイント：

* `GET /api/health`
* `POST /api/predict`
* `GET /`
* `GET /{full_path:path}`

`GET /` および `GET /{full_path:path}` では、React build後の `frontend/dist/index.html` を返します。

### `app/schemas.py`

APIの入力・出力データ構造を定義しています。

* `PredictRequest`
* `PredictResponse`

### `app/services/predictor.py`

感情分析モデルを読み込み、推論を行う処理を定義しています。

主な役割：

* `app/models/sentiment_model.joblib` の読み込み
* 入力テキストの推論
* 予測ラベルとスコアの返却

FastAPI起動時に学習済みモデルを読み込み、リクエストごとにそのモデルを使って推論します。

### `app/models/sentiment_model.joblib`

scikit-learnで学習した感情分析モデルです。

このファイルには、以下が含まれます。

* `TfidfVectorizer`
* `LogisticRegression`
* scikit-learn `Pipeline`

### `scripts/train_model.py`

学習データを読み込み、scikit-learnモデルを学習・評価して保存するスクリプトです。

主な処理：

* `data/sentiment_samples.csv` の読み込み
* `text` と `label` の分離
* `TfidfVectorizer` による文章の数値化
* `LogisticRegression` による分類モデルの学習
* train/test splitによる簡易評価
* `classification_report` によるクラス別評価
* 全データでの最終モデル再学習
* `joblib` によるモデル保存

### `frontend/src/App.tsx`

React + TypeScriptで作成した画面です。

主な役割：

* 入力テキストの状態管理
* サンプル入力ボタンの表示
* サンプルボタン押下時の入力欄更新
* Analyzeボタンの処理
* `fetch` による FastAPI へのPOSTリクエスト
* APIレスポンスの画面表示
* ローディング状態の管理
* エラー状態の管理
* 判定ラベルに応じた表示切り替え

### `frontend/src/App.test.tsx`

Frontendの基本的な表示と操作をテストするファイルです。

主な確認内容：

* タイトルが表示されるか
* 入力欄とAnalyzeボタンが表示されるか
* サンプル入力ボタンが表示されるか
* サンプルボタンをクリックすると入力欄の値が変わるか

### `tests/test_predictor.py`

推論ロジックを直接テストするファイルです。

主な確認内容：

* positive文が `positive` と判定されるか
* `not good` が `negative` と判定されるか
* `not bad` が `positive` と判定されるか
* `predict_sentiment()` の返り値に `text` / `label` / `score` が含まれているか

### `tests/test_api.py`

FastAPIのAPIエンドポイントをテストするファイルです。

主な確認内容：

* `GET /api/health` が `200` を返すか
* `POST /api/predict` が正常なJSONを返すか
* 不正なリクエストボディに対して `422` が返るか

## Machine Learning

このプロジェクトでは、scikit-learnを用いた感情分析モデルを使用しています。

### Training Data

学習データは以下に配置しています。

```text
data/sentiment_samples.csv
```

CSVは以下の形式です。

```csv
text,label
I love this product,positive
This is terrible,negative
It is okay,neutral
```

否定表現への対応を改善するため、以下のようなデータも含めています。

```text
This is not good,negative
This is not great,negative
This is not bad,positive
The product is neither good nor bad,neutral
```

### Feature Extraction

文章の数値化には `TfidfVectorizer` を使用しています。

現在は、単語単体だけでなく2語のまとまりも特徴量として扱うため、以下の設定を使用しています。

```python
TfidfVectorizer(ngram_range=(1, 2))
```

これにより、以下のような違いを学習しやすくしています。

```text
good      -> positive寄り
not good  -> negative寄り

bad       -> negative寄り
not bad   -> positive寄り
```

### Model Evaluation

`scripts/train_model.py` では、モデル保存前に簡易的な評価を行います。

評価では、学習データを train / test に分割し、test データに対する予測結果から以下を表示します。

```text
Accuracy
Classification report
```

`classification_report` では、各クラスごとに以下を確認できます。

* precision
* recall
* f1-score
* support

現在のデータセットは小規模なサンプルデータであるため、評価値は安定しません。
そのため、現時点の評価は実用性能を正確に測るものではなく、モデル評価の流れを確認するためのものです。

評価後、APIで使用する最終モデルは、全データで再学習して `app/models/sentiment_model.joblib` に保存します。

### Retraining

ローカル環境で以下を実行します。

```bash
source .venv/bin/activate
pip install -r requirements.txt
python scripts/train_model.py
```

モデルが更新されたら、Dockerコンテナを再buildします。

```bash
docker compose up --build
```

## Local Development

### Dockerで起動する

プロジェクト直下で以下を実行します。

```bash
docker compose up --build
```

起動後、以下にアクセスします。

```text
http://127.0.0.1:8080
```

APIドキュメントは以下で確認できます。

```text
http://127.0.0.1:8080/docs
```

ヘルスチェックAPIは以下です。

```text
http://127.0.0.1:8080/api/health
```

### FrontendとBackendを分けて起動する場合

開発中にReactのHot Reloadを使いたい場合は、FrontendとBackendを別々に起動できます。

Backend:

```bash
uvicorn app.main:app --reload
```

Backendは以下で起動します。

```text
http://127.0.0.1:8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Frontendは以下で起動します。

```text
http://localhost:5173
```

この開発時構成では、FrontendとBackendが別オリジンになります。
そのため、Viteのproxy設定で `/api` へのリクエストを `http://127.0.0.1:8000` に転送しています。

## Testing

### Backend Tests

Backendのテストはpytestで実行します。

```bash
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

### Frontend Tests

FrontendのテストはVitestで実行します。

```bash
cd frontend
npm ci
npm run test:run
```

### Test Coverage in This Project

Backendでは以下を確認しています。

* 推論関数の返り値
* `positive` / `negative` / `neutral` の基本判定
* `not good` / `not bad` の判定
* `/api/health` のレスポンス
* `/api/predict` のレスポンス
* 不正なリクエストに対する `422` レスポンス

Frontendでは以下を確認しています。

* タイトル表示
* 入力欄表示
* Analyzeボタン表示
* サンプル入力ボタン表示
* サンプルボタンクリック時の入力欄更新

## API

### GET `/api/health`

ヘルスチェック用エンドポイントです。

レスポンス例：

```json
{
  "message": "Hello, FastAPI"
}
```

### POST `/api/predict`

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

## CI/CD

このプロジェクトでは、GitHub Actionsを用いて自動テストとCloud Runへの自動デプロイを行っています。

### App Tests

以下のworkflowでBackendとFrontendのテストを実行します。

```text
.github/workflows/backend-test.yml
```

このworkflowでは、pushやPull Request作成時に以下を実行します。

```text
backend-test
→ pytest

frontend-test
→ npm ci
→ npm run test:run
```

### Cloud Run Auto Deploy

Cloud Runへの自動デプロイは、以下のworkflowで実行されます。

```text
.github/workflows/deploy-cloud-run.yml
```

このworkflowでは、`main` にアプリ本体の変更が入ったときに以下を実行します。

```text
1. リポジトリをcheckoutする
2. Pythonをセットアップする
3. requirements.txt をインストールする
4. pytest を実行する
5. Google Cloudに認証する
6. Cloud Runへデプロイする
```

テストが失敗した場合、Cloud Runへのデプロイは実行されません。

また、`paths` 条件により、READMEやスクリーンショットのみの変更ではCloud Runデプロイが走らないようにしています。

### GitHub Actions Variables

Cloud Runデプロイに必要な設定値は、workflowファイルに直接書かず、GitHub ActionsのRepository Variablesとして管理しています。

使用している主なVariablesは以下です。

```text
GCP_PROJECT_ID
GCP_REGION
CLOUD_RUN_SERVICE
GCP_WORKLOAD_IDENTITY_PROVIDER
GCP_SERVICE_ACCOUNT
```

### Google Cloud Authentication

GitHub ActionsからGoogle Cloudへの認証には、Workload Identity Federationを使用しています。

これにより、サービスアカウントキーJSONをGitHub Secretsに保存せずに、GitHub ActionsからGoogle Cloudへ認証しています。

### Deployment Flow

全体の流れは以下です。

```text
feature branch
↓
Pull Request
↓
App Tests
├── backend-test
└── frontend-test
↓
merge to main
↓
Deploy to Cloud Run workflow
↓
pytest
↓
Cloud Run deploy
↓
public URL updated
```

## Cloud Run Deployment

このアプリはCloud Runにデプロイしています。

Cloud Runでは、コンテナ化されたアプリケーションをGoogle Cloud上で実行できます。
このプロジェクトでは、React frontendをbuildし、その成果物をFastAPI backendから配信する一体型Docker構成をCloud Runにデプロイしています。

### Cloud Run向けのポート設定

Cloud Runでは、コンテナが環境変数 `PORT` で指定されたポートで待ち受ける必要があります。

そのため、Dockerfileでは以下のようにUvicornを起動しています。

```dockerfile
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
```

Cloud Run上では `PORT` 環境変数が使われ、ローカルではデフォルトで `8080` が使われます。

### 手動デプロイ

プロジェクト直下で以下を実行します。

```bash
gcloud run deploy ai-sentiment-web-app \
  --source . \
  --region asia-northeast1 \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 3
```

### デプロイ後の確認

デプロイが成功すると、以下のようなURLが表示されます。

```text
https://ai-sentiment-web-app-xxxxx-an.a.run.app
```

以下を確認します。

```text
https://<cloud-run-service-url>/
https://<cloud-run-service-url>/api/health
```

### ログ確認

Cloud Runのログは以下で確認できます。

```bash
gcloud run services logs read ai-sentiment-web-app \
  --region asia-northeast1
```

## Docker

このプロジェクトでは、multi-stage build を使用しています。

### Frontend build stage

Node.js環境でReactをbuildします。

```text
frontend/src
↓
npm run build
↓
frontend/dist
```

### Backend runtime stage

Python環境でFastAPIを起動します。

Frontend build stageで生成した `frontend/dist` をFastAPIコンテナへコピーし、FastAPIから静的ファイルとして配信します。

最終的なコンテナには以下が含まれます。

```text
/app
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── services/
│   └── models/
└── frontend/
    └── dist/
        ├── index.html
        └── assets/
```

## Notes

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

### scikit-learnモデルの制限

現在のモデルは、小規模なサンプルデータを用いた学習モデルです。

そのため、実用的な精度には達していません。

特に、複雑な否定表現や長文、未知語に対する予測は不安定です。

## What I Learned

このプロジェクトを通じて、以下を学習しました。

* FastAPIによるAPI設計
* Pydanticによるリクエスト・レスポンスの型定義
* React + TypeScriptによるFrontend実装
* Reactの状態管理
* Fetch APIによるFrontend / Backend連携
* scikit-learnによるモデル学習・保存・推論
* TF-IDFによるテキスト特徴量化
* train/test splitとclassification reportによるモデル評価
* Docker multi-stage build
* FastAPIによるReact build成果物の配信
* pytestによるBackendテスト
* Vitest / React Testing LibraryによるFrontendテスト
* GitHub ActionsによるCI
* Cloud Runへのデプロイ
* Workload Identity FederationによるGitHub ActionsからGoogle Cloudへの認証
* CI/CD構成
* Cloud Runのmin/max instancesによる基本的なコスト対策

## Current Limitations

* 学習データが小規模であり、実用的な精度には達していません
* 英文テキストのみを想定しています
* 否定表現は一部改善していますが、複雑な文脈理解はできません
* 未知語や長文に対する予測は不安定です
* 評価データも小規模であるため、評価指標は安定しません
* Frontendのテストは基本表示とサンプル操作に限定しています

## Future Improvements

* 学習データの追加
* より大きな公開データセットの利用
* モデル比較
* 日本語テキストへの対応
* Backendテストの拡充
* Frontendテストの拡充
* UI/UX改善
* Cloud Run自動デプロイのさらなる最適化
