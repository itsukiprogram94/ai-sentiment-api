from fastapi.testclient import TestClient

from app.main import app

#テスト用リクエスト
#Uvicornを起動しなくても、コード上でAPIを呼べるようにするためのクラス
client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI"}


def test_predict_api_positive():
    response = client.post(
        "/api/predict",
        json={"text": "This product is excellent"},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["text"] == "This product is excellent"
    assert data["label"] == "positive"
    assert isinstance(data["score"], float)


def test_predict_api_negative_with_negation():
    response = client.post(
        "/api/predict",
        json={"text": "This is not good"},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["label"] == "negative"

#テスト用のリクエストで、textキーがない場合のバリデーションエラーをテストする
#不正な入力を受けたときに、APIがちゃんとエラーを返すかを確認するためのテスト
def test_predict_api_validation_error():
    response = client.post(
        "/api/predict",
        json={"message": "This product is excellent"},
    )

    assert response.status_code == 422