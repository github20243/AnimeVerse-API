from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from anime_data import anime_list, AnimeBase

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/api/anime")
async def get_anime(
    search: Optional[str] = None,
    genre: Optional[str] = None,
    status: Optional[str] = None,
    type: Optional[str] = None,
    age_rating: Optional[str] = None,
    studio: Optional[str] = None,
    season: Optional[str] = None,
    min_rating: Optional[float] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = "desc",
    skip: int = 0,
    limit: int = 100
):
    filtered_anime = anime_list.copy()

    # Фильтрация
    if search:
        search = search.lower()
        filtered_anime = [
            anime for anime in filtered_anime
            if search in anime.title.lower() or 
               search in anime.description.lower() or
               search in anime.japanese_title.lower()
        ]

    if genre:
        filtered_anime = [
            anime for anime in filtered_anime
            if genre in anime.genre
        ]

    if status:
        filtered_anime = [
            anime for anime in filtered_anime
            if anime.status.lower() == status.lower()
        ]

    if type:
        filtered_anime = [
            anime for anime in filtered_anime
            if anime.type.lower() == type.lower()
        ]

    if age_rating:
        filtered_anime = [
            anime for anime in filtered_anime
            if anime.age_rating == age_rating
        ]

    if studio:
        filtered_anime = [
            anime for anime in filtered_anime
            if anime.studio.lower() == studio.lower()
        ]

    if season:
        filtered_anime = [
            anime for anime in filtered_anime
            if anime.season.lower() == season.lower()
        ]

    if min_rating is not None:
        filtered_anime = [
            anime for anime in filtered_anime
            if anime.rating >= min_rating
        ]

    # Сортировка
    if sort_by:
        reverse = sort_order.lower() == "desc"
        filtered_anime.sort(
            key=lambda x: getattr(x, sort_by),
            reverse=reverse
        )

    # Пагинация
    return filtered_anime[skip : skip + limit]

@app.get("/api/anime/{anime_id}")
async def get_anime_by_id(anime_id: int):
    for anime in anime_list:
        if anime.id == anime_id:
            return anime
    raise HTTPException(status_code=404, detail="Anime not found")

@app.get("/api/genres")
async def get_genres():
    genres = set()
    for anime in anime_list:
        genres.update(anime.genre)
    return {"genres": sorted(list(genres))}

@app.get("/api/studios")
async def get_studios():
    studios = set(anime.studio for anime in anime_list)
    return {"studios": sorted(list(studios))}

@app.get("/api/types")
async def get_types():
    types = set(anime.type for anime in anime_list)
    return {"types": sorted(list(types))}

@app.get("/api/age_ratings")
async def get_age_ratings():
    ratings = set(anime.age_rating for anime in anime_list)
    return {"age_ratings": sorted(list(ratings))}

@app.get("/api/seasons")
async def get_seasons():
    seasons = set(anime.season for anime in anime_list)
    return {"seasons": sorted(list(seasons))}

@app.get("/api/anime/{anime_id}/comments")
async def get_comments(anime_id: int):
    return [comment for comment in comments_db if comment.anime_id == anime_id]

@app.post("/api/anime/{anime_id}/comments")
async def add_comment(anime_id: int, comment: CommentBase):
    global comment_counter
    for anime in anime_list:
        if anime.id == anime_id:
            comment_counter += 1
            new_comment = Comment(
                id=comment_counter,
                anime_id=anime_id,
                **comment.dict()
            )
            comments_db.append(new_comment)
            
            # Обновляем рейтинг аниме
            anime_comments = [c for c in comments_db if c.anime_id == anime_id]
            total_rating = sum(c.rating for c in anime_comments)
            anime.rating = total_rating / len(anime_comments)
            
            return new_comment
    raise HTTPException(status_code=404, detail="Anime not found")

@app.post("/api/anime/{anime_id}/view")
async def increment_views(anime_id: int):
    for anime in anime_list:
        if anime.id == anime_id:
            anime.views += 1
            return {"views": anime.views}
    raise HTTPException(status_code=404, detail="Anime not found")
