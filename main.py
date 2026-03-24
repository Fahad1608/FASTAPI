from fastapi import FastAPI
from pydantic import BaseModel
import base64
import requests

app = FastAPI()

# 🔐 Hardcoded Azure Credentials
CLIENT_ID = "a93afcea-d71e-4823-ad70-96535fdd68c1"
TENANT_ID = "63bd2f99-4c32-47eb-b492-a486ad89754e"
CLIENT_SECRET = "Q8E8Q~Yr9OSyT.0mG74uhwvz9xd4km4lTUoUMazT"

# 📂 Hardcoded SharePoint Details
SITE_ID = "liongard.sharepoint.com,30624ea5-37e8-4ae6-a3fa-948ef66cbeed,0936933d-88a8-45e4-980d-2e1c9adf2730"
DRIVE_ID = "b!pU5iMOg35kqj-pSO9my-7T2TNgmoiORFmA0uHJrfJzCkLel8VkwAR4BEzi1g87A-"

# 🔑 Token Endpoint
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"


class FilePayload(BaseModel):
    fileName: str
    fileContent: str  # Base64 encoded


@app.get("/")
def home():
    return {"status": "running"}


def get_access_token():
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(TOKEN_URL, data=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Token Error: {response.text}")

    return response.json()["access_token"]


@app.post("/upload")
def upload_file(payload: FilePayload):

    # 🔑 Generate token dynamically
    access_token = get_access_token()

    # 📦 Decode base64 file
    binary_data = base64.b64decode(payload.fileContent)

    # 📂 Upload directly to ROOT
    upload_url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/root:/{payload.fileName}:/content"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream"
    }

    response = requests.put(upload_url, headers=headers, data=binary_data)

    return {
        "status_code": response.status_code,
        "response": response.text
    }
