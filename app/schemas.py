#APIの入力と出力の型定義を行うファイル
from pydantic import BaseModel

#API入力の型定義
class PredictRequest(BaseModel):
    text: str 

#API出力の型定義
class PredictResponse(BaseModel):
    text: str
    label: str
    score: float