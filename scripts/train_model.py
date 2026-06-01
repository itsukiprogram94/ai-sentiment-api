from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


DATA_PATH = Path("data/sentiment_samples.csv")
MODEL_DIR = Path("app/models")
MODEL_PATH = MODEL_DIR / "sentiment_model.joblib"
RANDOM_STATE = 42


def create_model() -> Pipeline:
    return Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
            ("classifier", LogisticRegression(max_iter=1000)),
        ]
    )

def evaluate_model(x:pd.Series, y: pd.Series) -> None:
    x_train, x_test, y_train, y_test = train_test_split(
        x, 
        y, 
        test_size=0.25, 
        random_state=RANDOM_STATE, 
        stratify=y
    )

    model = create_model()
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("Evaluation result")
    print("=================")
    print(f"Accuracy: {accuracy:.3f}")
    print()
    print("Classification report")
    print("=====================")
    print(classification_report(y_test, y_pred))


def train_final_model(x: pd.Series, y: pd.Series) -> Pipeline:
    model = create_model()
    model.fit(x, y)
    return model


def train_model() -> None:   
    df = pd.read_csv(DATA_PATH)

    x = df["text"]
    y = df["label"]
    evaluate_model(x, y)
    final_model = train_final_model(x, y)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(final_model, MODEL_PATH)

    print(f"Model saved to {MODEL_PATH}")



if __name__ == "__main__":
    train_model()
