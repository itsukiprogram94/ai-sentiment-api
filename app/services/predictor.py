from pathlib import Path
import joblib

MODEL_PATH = Path("app/models/sentiment_model.joblib")

model = joblib.load(MODEL_PATH)




#戻り値をdict(辞書型)で返すように関数を定義する
def predict_sentiment(text: str) -> dict:
    predicted_label = model.predict([text])[0]

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba([text])[0]
        class_labels = model.classes_
        
        #ラベルと確率を対応させる
        label_to_probability = dict(zip(class_labels, probabilities))
        score = float(label_to_probability[predicted_label])
    else:
        score = 1.0

    return {
        "text": text,
        "label": predicted_label,
        "score": round(score, 3),
    }