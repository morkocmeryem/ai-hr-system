# affinda/parser.py
import httpx

AFFINDA_API_URL = "https://api.affinda.com/v1/documents"
AFFINDA_API_KEY = "HRsystem"

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
