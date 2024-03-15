# schemas.py
from pydantic import BaseModel
from fastapi import File, UploadFile
from typing import List, Union, Optional


# 1. 모델 정보 요청 응답 데이터 모델
class ModelInfoResponse(BaseModel):
    models: List[str]

# 2. 모델 훈련 요청 데이터 모델
class TrainModelRequest(BaseModel):
    model_name: str
    audios: Optional[UploadFile] = File(None)

# 3. 텍스트 정보 요청 데이터 모델
class TextInfoRequest(BaseModel):
    text: str

# 4. 모델 추론 결과 응답 데이터 모델
class PredictionResponse(BaseModel):
    input_data: str
    prediction: str

# 5. 모든 데이터 초기화
class ResetDataRequest(BaseModel):
    models: List[str]
    model_name: str
    text: str
    
    