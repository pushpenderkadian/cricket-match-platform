from pydantic import BaseModel
from typing import Optional

class Match(BaseModel):
    t1f: str
    t2f: str
    fid: int
    date: str
    status: int
    mf: str
    s1: Optional[str] = None
    s2: Optional[str] = None
    result: Optional[str] = None

class LiveData(BaseModel):
    match_id: str
    score: str
    details: str
    status: str
