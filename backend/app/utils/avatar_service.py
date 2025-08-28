import os
import time
import uuid
import base64
import requests
from azure.storage.blob import BlobServiceClient

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")
STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT")
STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
PERM_CONTAINER = os.getenv("PERM_CONTAINER")

blob_service = BlobServiceClient(
    account_url=f"https://{STORAGE_ACCOUNT}.blob.core.windows.net",
    credential=STORAGE_KEY
)


SYSTEM_PROMPT = (
    "You are generating a profile avatar image for a user. "
    "The image should be a head-and-shoulders portrait, well-lit, centered, "
    "and suitable for use as a profile picture. "
    "Keep the background simple or blurred. "
    "Focus on clear facial features and a friendly expression."
)


def generate_avatar(prompt: str, style: str) -> str:
    """Generate avatar image from prompt and return temporary blob URL."""
    url = f"{AZURE_OPENAI_ENDPOINT}"
    headers = {
        "Authorization": f"Bearer {AZURE_OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DEPLOYMENT_NAME,
        "prompt": f"{SYSTEM_PROMPT} User input: {prompt}",
        "size": "1024x1024",
        "style": style,
        "quality": "standard",
        "n": 1
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    return response.json()["data"][0]["url"]


def approve_avatar(temp_url: str, user_id: str, old_avatar_url: str | None) -> str:
    """Download image from temp URL, store in permanent blob container, delete old avatar if exists."""
    if not temp_url:
        remove_avatar(old_avatar_url)
        return temp_url

    if temp_url == old_avatar_url:
        return temp_url

    try:
        response = requests.get(temp_url)
        response.raise_for_status()
        image_bytes = response.content
    except Exception as e:
        return old_avatar_url or ""

    timestamp = int(time.time())
    perm_blob_name = f"{user_id}_v{timestamp}.png"

    perm_blob_client = blob_service.get_blob_client(
        container=PERM_CONTAINER, blob=perm_blob_name
    )
    perm_blob_client.upload_blob(image_bytes, overwrite=True)

    remove_avatar(old_avatar_url)

    return perm_blob_client.url


def remove_avatar(avatar_url: str | None):
    if avatar_url:
        blob_name = avatar_url.split("/")[-1]
        blob_client = blob_service.get_blob_client(
            container=PERM_CONTAINER, blob=blob_name
        )
        if blob_client.exists():
            blob_client.delete_blob(delete_snapshots="include")
