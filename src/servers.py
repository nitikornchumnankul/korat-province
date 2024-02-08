from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json
import os
import requests
import json
import pandas as pd



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

## get data from nakhon_ratchasima.json on local using get method
def read_raw_database():
    with open('../data/nakhon_ratchasima.json', 'r') as f:
        raw_database = json.load(f)
    return raw_database
data = read_raw_database()    


# f method by id using ampore and distric
def read_code(district: str):
    url="https://opend.data.go.th/govspending/egpdepartment"
    api_key = ""
    params = {
        "api-key": api_key,
        "dept_name": district
    }
    response = requests.get(url,params=params)
    data = response.json()
    df = pd.DataFrame(data['result'])
    df = df[df['dept_name'].str.contains('^เทศบาลตำบล', regex=True)]
    dept_code = df['dept_code'].values[0]
    return dept_code

def read_prices(dept_code: str, year: str):
    url = 'https://opend.data.go.th/govspending/summary_cgdcontract'
    api_key = ""
    params = {
        "api-key": api_key,
        "year": year,
        "dept_code": dept_code
    }
    response = requests.get(url,params=params)
    data = response.json()
    return data


@app.get("/nakhon_ratchasima")
async def get_nakhon_ratchasima():
    async with httpx.AsyncClient() as client:
        ## read data from read_raw_database
        data = read_raw_database()
        return data
       
# get method by id using ampore and distric
@app.get("/nakhon_ratchasima/{district}/{years}")
async def get_nakhon_ratchasima(district: str, years: str):
     code = read_code(district)
     price = read_prices(code, years)
     return price
    
 
    