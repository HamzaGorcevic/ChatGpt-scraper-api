
from fastapi import APIRouter
from models.message import Message
from scraper.logic import scrape_gpt
router = APIRouter()

@router.post("/chatgpt")

async def scrape(request:Message):
    response = scrape_gpt(request.message)
    return response