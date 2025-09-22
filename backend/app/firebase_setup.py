import firebase_admin
from firebase_admin import credentials, auth
import os
from fastapi import Depends, HTTPException, Header
from dotenv import load_dotenv

load_dotenv()

cred = credentials.Certificate("app/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

def fb_verify_token(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = authorization.split(" ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
