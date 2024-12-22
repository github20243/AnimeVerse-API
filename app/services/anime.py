from typing import List, Optional
from ..models.anime import CommentBase, AnimeComment
from anime_data import anime_list

def get_anime_list():
    return anime_list

def get_anime_by_id(anime_id: int):
    return next((anime for anime in anime_list if anime.id == anime_id), None)

def add_comment_to_anime(anime_id: int, comment: CommentBase):
    anime = get_anime_by_id(anime_id)
    if not anime:
        return None
    if not hasattr(anime, 'comments'):
        anime.comments = []
    anime.comments.append(comment)
    return comment

def get_unique_values(field: str) -> List[str]:
    values = set()
    for anime in anime_list:
        if field == 'genres':
            values.update(getattr(anime, field, []))
        else:
            values.add(getattr(anime, field, None))
    return sorted(list(filter(None, values)))
