from fastapi import APIRouter
from backend.database import scorecard_collection
from backend.scraper import get_scorecard

router = APIRouter()


@router.get("/scorecard/{match_id}")
async def get_live_scorecard(match_id: str):
    data=scorecard_collection.find_one({"match_id": match_id}, {"_id": 0})
    if data:
        return data.get("match_data")
    else:
        scorecard=get_scorecard(match_id)
        return scorecard

            
    