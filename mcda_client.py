import os
import httpx
from dotenv import load_dotenv

load_dotenv()
BASE_API_URL = os.getenv("MCDA_API_URL") or "http://127.0.0.1:8000"

class MCDAClient:
    def __init__(self, base_api_url: str = BASE_API_URL):
        self.base_api_url = base_api_url

    async def check_data_availability(self) -> dict:
        """Check the DB whether process data are available or not."""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_api_url}/DB/available-applications")
                response.raise_for_status()
                return {"Data": response.json()}
        except Exception as e:
            return {"error": str(e)}

    async def get_process_data(self, process: str) -> dict:
        """Retrieve data for a particular process."""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(
                    f"{self.base_api_url}/DB/application/specified?application={process}"
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {"error": str(e)}
