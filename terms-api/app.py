from fastapi import FastAPI, Request
from transformers import pipeline

app = FastAPI()

# Load summarizer model once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.get("/")
def root():
    return {"message": "API running"}

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    text = data.get("text", "")

    if not text:
        return {"error": "No text provided"}

    summary = summarizer(text, max_length=200, min_length=50, do_sample=False)[0]['summary_text']

    # simple risk scan
    risky_words = ["third party", "data share", "penalty", "auto-renew"]
    risk = "green"
    for w in risky_words:
        if w in text.lower():
            risk = "red"
            break

    return {
        "summary": summary,
        "risk": risk,
        "hindi": "TODO: integrate translation later"
    }
