from fastapi import FastAPI, UploadFile, File
from file_handler import extract_text_from_file
from gpt_extractor import extract_financial_data
import uvicorn
import os

app = FastAPI()

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        text, _ = extract_text_from_file(temp_path)
        data = extract_financial_data(text)
        os.remove(temp_path)
        return {"result": data}
    except Exception as e:
        os.remove(temp_path)
        return {"error": str(e)}

# To run locally:
# uvicorn api:app --reload
