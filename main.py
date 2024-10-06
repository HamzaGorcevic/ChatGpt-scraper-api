from fastapi import FastAPI
from routes import chatgpt

app = FastAPI()

app.include_router(chatgpt.router,prefix="/api")
