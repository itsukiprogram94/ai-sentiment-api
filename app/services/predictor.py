#戻り値をdict(辞書型)で返すように関数を定義する
def predict_sentiment(text: str) -> dict:
    positive_words = ["love", "good", "great", "excellent", "happy"]
    negative_words = ["bad", "hate", "terrible", "sad", "poor"]

    lower_text = text.lower()

    if any(word in lower_text for word in positive_words):
        label = "positive"
        score = 0.9
    elif any(word in lower_text for word in negative_words):
        label = "negative"
        score = 0.9
    else:
        label = "neutral"
        score = 0.5

    return {
        "text": text,
        "label": label,
        "score": score,
    }