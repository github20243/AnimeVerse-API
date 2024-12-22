from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..models.anime import CommentBase, AnimeComment
from ..services.anime import get_anime_list, get_anime_by_id, add_comment_to_anime

router = APIRouter(prefix="/api/anime", tags=["anime"])

@router.get("/")
async def get_all_anime():
    return get_anime_list()

@router.get("/{anime_id}")
async def get_anime(anime_id: int):
    anime = get_anime_by_id(anime_id)
    if not anime:
        raise HTTPException(status_code=404, detail="Аниме не найдено")
    return anime

@router.post("/{anime_id}/comments")
async def add_comment(anime_id: int, comment: CommentBase):
    return add_comment_to_anime(anime_id, comment)

@router.get("/filter")
async def filter_anime(
    genre: Optional[str] = None,
    season: Optional[str] = None,
    year: Optional[int] = None,
    age_rating: Optional[str] = None
):
    anime_list = get_anime_list()
    
    if genre:
        anime_list = [anime for anime in anime_list if genre.lower() in [g.lower() for g in anime.genres]]
    if season:
        anime_list = [anime for anime in anime_list if season.lower() == anime.season.lower()]
    if year:
        anime_list = [anime for anime in anime_list if year == anime.year]
    if age_rating:
        anime_list = [anime for anime in anime_list if age_rating.lower() == anime.age_rating.lower()]
    
    return anime_list
