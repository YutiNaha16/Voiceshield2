from fastapi import FastAPI, UploadFile, File
import requests

app = FastAPI()

AI_MODEL_URL = "http://127.0.0.1:8000"

@app.post("/speech_to_text")
async def speech_to_text(file: UploadFile = File(...)):
    audio_data = await file.read()
    response = requests.post(f"{AI_MODEL_URL}/speech_to_text", files={"file": ("audio.wav", audio_data)})
    return response.json()

@app.post("/analyze_text")
async def analyze_text(data: dict):
    response = requests.post(f"{AI_MODEL_URL}/analyze_text", json=data)
    return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
