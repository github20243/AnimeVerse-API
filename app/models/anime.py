from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CommentBase(BaseModel):
    user_name: str
    text: str
    created_at: datetime = datetime.now()

class AnimeComment(BaseModel):
    anime_id: int
    comments: List[CommentBase] = []

class VideoQuality(BaseModel):
    quality: str
    url: str
