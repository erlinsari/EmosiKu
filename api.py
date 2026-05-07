from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

app = FastAPI()

# Izinkan Frontend React memanggil API ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model IndoBERT (Sama seperti di app.py Anda)
MODEL_NAME = "indobenchmark/indobert-base-p1"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
stopword_remover = StopWordRemoverFactory().create_stop_word_remover()

class TextRequest(BaseModel):
    text: str

def clean_text(text):
    if not isinstance(text, str): return ""
    # Cleaning sama persis dengan logika Anda
    text = re.sub(r'http\S+|www\S+|https\S+|@\w+|#\w+|[^a-zA-Z\s]', '', text, flags=re.MULTILINE).lower()
    return re.sub(r'\s+', ' ', stopword_remover.remove(text)).strip()

@app.post("/predict")
async def predict(request: TextRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Teks tidak boleh kosong")
    
    cleaned = clean_text(request.text)
    inputs = tokenizer(cleaned, return_tensors="pt", truncation=True, padding=True, max_length=128)
    
    with torch.no_grad():
        out = model(**inputs)
    
    probs = torch.softmax(out.logits, dim=-1)[0]
    pred = torch.argmax(out.logits, dim=-1).item()
    
    return {
        "prediction": pred, # 0: Stabil, 1: Terindikasi
        "confidence": float(probs[pred]),
        "probabilities": {
            "stable": float(probs[0]),
            "anxiety": float(probs[1])
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
