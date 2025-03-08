import streamlit as st
import requests
import os
import tempfile
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import sounddevice as sd
import wave

# Download necessary NLTK files
nltk.download("punkt")
nltk.download("stopwords")

BACKEND_URL = "http://127.0.0.1:5000"

# Custom CSS for Beautiful UI
st.markdown("""
    <style>
        body { background: linear-gradient(to right, #ff66b2, #9900cc); }
        .stApp { background: black; color: white; font-family: 'Arial', sans-serif; }
        .stTitle { color: #ff66b2; font-size: 40px; font-weight: bold; text-align: center;
                   padding: 15px; text-shadow: 0px 0px 10px rgba(255, 102, 178, 0.8); }
        .stHeader { color: #ff33cc; font-size: 26px; font-weight: bold; text-align: center;
                    text-shadow: 0px 0px 8px rgba(255, 51, 204, 0.6); }
        .stTextArea, .stTextInput { background: rgba(255, 255, 255, 0.1); border-radius: 15px;
                                    backdrop-filter: blur(10px); color: white !important; }
        .stButton>button { background: linear-gradient(to right, #ff33cc, #9900cc);
                           color: white; border-radius: 12px; padding: 12px 25px; font-size: 16px;
                           box-shadow: 0px 0px 15px rgba(255, 51, 204, 0.8); transition: all 0.3s ease-in-out; }
        .stButton>button:hover { transform: scale(1.05); box-shadow: 0px 0px 25px rgba(255, 51, 204, 1); }
    </style>
""", unsafe_allow_html=True)

# Page Title
st.markdown('<h1 class="stTitle">🎀🛡️ VoiceShield: AI-Powered Speech & Text Analysis 🎀</h1>', unsafe_allow_html=True)

# Function to record audio
def record_audio(duration=5, sample_rate=44100):
    st.write("🎙 Recording... Please speak")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
   
    # Save to temp file
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with wave.open(temp_audio.name, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())
   
    return temp_audio.name

# Function to analyze text
def analyze_text(text):
    response = requests.post(f"{BACKEND_URL}/analyze_text", json={"text": text})
    return response.json()

# Function to transcribe audio
def transcribe_audio(file_path):
    with open(file_path, "rb") as f:
        response = requests.post(f"{BACKEND_URL}/speech_to_text", files={"file": f})
    return response.json()

# Live Audio Recording
st.markdown('<h2 class="stHeader">🎙️ Live Voice Transcription</h2>', unsafe_allow_html=True)
if st.button("🎤 Start Recording"):
    audio_file_path = record_audio()
    st.success("✅ Recording complete! Transcribing...")
    result = transcribe_audio(audio_file_path)
    os.remove(audio_file_path)

    st.text_area("Transcribed Text", result["transcribed_text"], height=100)
    analysis = analyze_text(result["transcribed_text"])
    st.subheader("🔍 Analysis Result")
    st.json(analysis)

# Upload Audio File
st.markdown('<h2 class="stHeader">📂 Upload Audio</h2>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    result = transcribe_audio(temp_audio_path)
    os.remove(temp_audio_path)

    st.text_area("Transcribed Text", result["transcribed_text"], height=100)
    analysis = analyze_text(result["transcribed_text"])
    st.subheader("🔍 Analysis Result")

    st.json(analysis)

# Text Input Analysis
st.markdown('<h2 class="stHeader">💬 Enter Text for Analysis</h2>', unsafe_allow_html=True)
user_text = st.text_input("Enter text here:")
if user_text:
    analysis = analyze_text(user_text)
    st.subheader("🔍 Analysis Result")
    st.json(analysis)
