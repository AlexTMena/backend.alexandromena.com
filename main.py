from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app_name = os.getenv("APP_NAME")

@app.get("/")
async def home():
    print("home directory toggled")
    return {
        "message" : "App is up and running",
        "app" : app_name
    }