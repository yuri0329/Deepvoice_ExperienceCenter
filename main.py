# main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List
import schemas  # schemas.py 파일에서 정의한 모델을 import

app = FastAPI()

# 임시로 데이터를 저장할 딕셔너리
data = {
    "models": [],
    "model_name": None,
    "recordings": [],
    "text_info": None
}

# 0. 모델 리스트 받기
@app.get("/models")
async def get_models():
    return schemas.ModelInfoResponse(models=data["models"])  

# 1. 모델 훈련 이름 정보 받기 & 2. 녹음 파일 받기 (20개) 3. 모델 훈련 시작하기
@app.post("/train_model")
async def train_model(train_data: schemas.TrainModelRequest):  
    model_name = train_data.model_name
    audios = train_data.audios

    if len(audios) > 20:
        raise HTTPException(status_code=400, detail="Maximum recordings limit exceeded")

    for audio_file in audios:
        file_path = f"./uploads/{audio_file.filename}"
        with open(file_path, "wb") as audio_writer:
            audio_writer.write(audio_file.file.read())
            # train_result = train_model_function(model_name, file_path)

    return {"message": f"Model training completed for {model_name} with {len(audios)} audio files"}

        

# 4. 텍스트 정보 받기 6. 모델 추론 결과 제공
@app.post("/text_info")
async def text_info(text_data: schemas.TextInfoRequest):
    if not text_data.text:
        raise HTTPException(status_code=400, detail="No text provided")

    data["text_info"] = text_data.text
    return {"message": "Text information received"}

# 5. 모델 추론하기 - 현기코드 제공예정

# 6. 모델 추론 결과 제공 엔드포인트
@app.get("/prediction", response_model=schemas.PredictionResponse)
async def get_prediction():
    if data["text_info"] is None:
        return {"error": "No text information provided"}
    
    # 모델 추론 로직 구현
    prediction = run_inference(data["text_info"])  # 모델 추론 함수를 호출하여 예측 결과를 받기
    
    # 모델 추론 결과를 제공하는 부분
    return schemas.PredictionResponse(prediction=prediction)

# 7. 데이터 초기화
@app.delete("/reset_data")
async def reset_data(reset_data: schemas.ResetDataRequest):
    if not reset_data.models or not reset_data.model_name or not reset_data.text:
        raise HTTPException(status_code=400, detail="Missing required fields in reset data request")

    data["models"] = reset_data.models
    data["model_name"] = reset_data.model_name
    data["recordings"] = []
    data["text_info"] = reset_data.text
    return {"message": "All data reset"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)