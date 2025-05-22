from fastapi import FastAPI
from app.api import upload, query
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(upload.router)
app.include_router(query.router)
