import httpx

AFFINDA_API_URL = "https://api.affinda.com/v1/documents"
AFFINDA_API_KEY = "aff_9c5058f99dd6304e8d9185bbf9ea87ce70d64375 "  # <-- buraya kendi API key'ini gir

async def parse_cv(file_path: str):
    headers = {
        "Authorization": f"Bearer {AFFINDA_API_KEY}",
    }
    files = {
        'file': open(file_path, 'rb'),
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(AFFINDA_API_URL, headers=headers, files=files)
        response.raise_for_status()
        return response.json()
