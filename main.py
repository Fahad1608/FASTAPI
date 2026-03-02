from fastapi import FastAPI
from pydantic import BaseModel
import base64
import requests
import os

app = FastAPI()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
SITE_ID = os.getenv("SITE_ID")
DRIVE_ID = os.getenv("DRIVE_ID")

class FilePayload(BaseModel):
    fileName: str
    folderPath: str
    fileContent: str

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/upload")
def upload_file(payload: FilePayload):

    binary_data = base64.b64decode(payload.fileContent)

    upload_url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/root:/{payload.folderPath}/{payload.fileName}:/content"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/octet-stream"
    }

    response = requests.put(upload_url, headers=headers, data=binary_data)

    return {
        "status_code": response.status_code,
        "response": response.text
    }