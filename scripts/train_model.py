from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


DATA_PATH = Path("data/sentiment_samples.csv")
MODEL_DIR = Path("app/models")
MODEL_PATH = MODEL_DIR / "sentiment_model.joblib"


def train_model() -> None:   
    df = pd.read_csv(DATA_PATH)

    x = df["text"]
    y = df["label"]

    #Pipelineは機械学習の前処理とモデルを一連の流れで実行するためのクラス
    model = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),#テキストデータを数値化するための前処理
            ("classifier", LogisticRegression(max_iter=1000)),#ロジスティック回帰モデルを使用して、テキストデータの感情を分類するための機械学習アルゴリズム
        ]
    )

    model.fit(x, y)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train_model()
