from fastapi import FastAPI, Depends
import os
from dotenv import load_dotenv

from backend.firebase_setup import fb_verify_token
load_dotenv()

app = FastAPI(title="Next-Step Backend")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Next-Step Backend!"}

@app.get("/protected")
def protected_route(user_data: dict = Depends(fb_verify_token)):
    return {"message": "Hello, secure world!", "user": user_data["uid"]}
