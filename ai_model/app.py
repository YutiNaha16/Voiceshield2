from fastapi import FastAPI, UploadFile, File
import whisper
from transformers import pipeline
import io
import soundfile as sf
import textstat
from nltk.tokenize import word_tokenize
from collections import Counter
import nltk

# Download NLTK data
nltk.download("punkt")
nltk.download("stopwords")

app = FastAPI()

# Load AI Models
whisper_model = whisper.load_model("small")
sentiment_pipeline = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Function to analyze text (Sentiment + Readability)
def analyze_text(text):
    sentiment_result = sentiment_pipeline(text)[0]
    sentiment = "Positive 😊" if sentiment_result["label"] == "POSITIVE" else "Negative 😡"
    sentiment_score = round(sentiment_result["score"], 2)

    # Keyword Extraction
    words = word_tokenize(text.lower())
    keyword_counts = Counter(words)
    keywords = [word for word, count in keyword_counts.most_common(5)]

    # Readability Score
    flesch_score = textstat.flesch_reading_ease(text)
    readability = "Easy 😊" if flesch_score >= 60 else "Difficult 📚"

    return {
        "Sentiment": sentiment,
        "Sentiment Score": sentiment_score,
        "Keywords": keywords,
        "Readability": readability,
    }

# Speech-to-Text Endpoint
@app.post("/speech_to_text")
async def speech_to_text(file: UploadFile = File(...)):
    audio_data = await file.read()
    audio_file = io.BytesIO(audio_data)
    audio, sample_rate = sf.read(audio_file, dtype="float32")

    # Whisper Transcription
    result = whisper_model.transcribe(audio)

    return {"transcribed_text": result["text"]}

# Text Analysis Endpoint
@app.post("/analyze_text")
async def analyze_text_endpoint(data: dict):
    text = data["text"]
    return analyze_text(text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
