from fastapi import APIRouter, Query
import datetime
from backend.database import matches_collection

router = APIRouter()

@router.get("/matches-list")
async def get_matches(page: int = Query(1, alias="page", ge=1), page_size: int = Query(10, alias="page_size", ge=1, le=100)):
    # Get today's timestamp at 12:01 AM
    current_time = datetime.datetime.now().replace(hour=0, minute=1, second=0, microsecond=0).timestamp()

    # Calculate skip value
    skip_count = (page - 1) * page_size

    # Fetch paginated matches
    matches_cursor = (
        matches_collection.find({"t": {"$gt": current_time}}, {"_id": 0})
        .sort("t", 1)
        .skip(skip_count)
        .limit(page_size)
    )

    # Convert cursor to list
    matches = list(matches_cursor)

    return {"page": page, "page_size": page_size, "matches": matches}
