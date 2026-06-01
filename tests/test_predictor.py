from app.services.predictor import predict_sentiment


def test_predict_sentiment_positive():
    result = predict_sentiment("This product is excellent")

    assert result["text"] == "This product is excellent"
    assert result["label"] == "positive"
    assert isinstance(result["score"], float)


def test_predict_sentiment_negative_with_negation():
    result = predict_sentiment("This is not good")

    assert result["label"] == "negative"
    assert isinstance(result["score"], float)


def test_predict_sentiment_positive_with_negation():
    result = predict_sentiment("This is not bad")

    assert result["label"] == "positive"
    assert isinstance(result["score"], float)


def test_predict_sentiment_response_keys():
    result = predict_sentiment("The product arrived today")

    assert set(result.keys()) == {"text", "label", "score"}
    