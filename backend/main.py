from fastapi import FastAPI, Form
import requests

app = FastAPI()

def query_llama(prompt: str):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama2", "prompt": prompt, "stream": False}
    )
    return response.json()["response"].strip()

@app.post("/extract/")
def extract_medical_info(note: str = Form(...)):
    prompt = (
        f"Extract the following from the doctor's note:\n"
        f"- Symptoms\n- Diagnosis\n- Medications\n- Follow-up Instructions\n"
        f"Return the output in JSON format.\n\nNote:\n{note}"
    )
    structured_data = query_llama(prompt)
    return {"structured": structured_data}
