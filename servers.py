from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# Define a list of origins that should be permitted to make cross-origin requests.
origins = [
    "http://localhost:3000",  # Add other origins as needed
    "http://127.0.0.1:3000",  # You can also specify ports.
]

# Add CORSMiddleware to the application instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

api_key = ""
base_url = "https://opend.data.go.th/govspending/summary_cgdcontract"

@app.get("/get-contract-summary")
async def get_contract_summary(year: int = 2566, dept_code: int = 6300801):
    params = {
        "api-key": api_key,
        "year": year,
        "dept_code": dept_code
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)
        return response.json()