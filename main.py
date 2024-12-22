from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.routers import anime
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from anime_data import anime_list, AnimeBase
import os

app = FastAPI(
    title="AniCore API",
    description="API для аниме сайта с поддержкой комментариев и видео",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS
origins = [
    "http://localhost:8080",
    "http://localhost:3000",
    "https://anime-site-nurs.vercel.app",  # Ваш реальный домен фронтенда
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

class CommentBase(BaseModel):
    user_name: str
    text: str
    rating: float
    created_at: datetime = datetime.now()

class Comment(CommentBase):
    id: int
    anime_id: int

# Глобальное хранилище комментариев
comments_db = []
comment_counter = 0

# Подключаем роутеры
app.include_router(anime.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
