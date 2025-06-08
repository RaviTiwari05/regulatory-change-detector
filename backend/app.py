from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from change_detector import detect_changes
from llm_analyzer import analyze_change

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze/")
async def analyze_changes(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    text1 = (await file1.read()).decode("utf-8")
    text2 = (await file2.read()).decode("utf-8")

    changes = detect_changes(text1, text2)
    results = []

    for change in changes:
        analysis = analyze_change(change)
        results.append({
            "change_type": analysis.get("change_type", "Ambiguous"),
            "change_summary": analysis.get("change_summary", "No summary available.")
        })

    print("Final response to frontend:", results)  
    return {"results": results}
