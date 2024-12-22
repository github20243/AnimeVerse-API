from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class VideoSource(BaseModel):
    quality: str
    url: str

class AnimeBase(BaseModel):
    id: int
    title: str
    japanese_title: str
    description: str
    image_url: str
    episodes: int
    status: str
    genre: List[str]
    rating: float
    studio: str
    duration: str
    season: str
    video_sources: dict
    comments: List[str]
    total_ratings: int
    average_rating: float
    age_rating: str
    type: str
    next_episode_date: Optional[str]
    popularity_rank: int
    views: int

anime_list = [
    AnimeBase(
        id=1,
        title="Attack on Titan",
        japanese_title="進撃の巨人",
        description="В мире, где человечество живет внутри городов, окруженных огромными стенами из-за гигантов, пожирающих людей, юный Эрен Йегер намерен изменить этот мир.",
        image_url="https://cdn.myanimelist.net/images/anime/10/47347.jpg",
        episodes=25,
        status="Завершён",
        genre=["Экшен", "Драма", "Фэнтези"],
        rating=9.0,
        studio="Wit Studio",
        duration="24 мин",
        season="Весна 2013",
        video_sources={
            "1080p": "https://video.sibnet.ru/shell.php?videoid=3232547",
            "720p": "https://video.sibnet.ru/shell.php?videoid=3232547",
            "480p": "https://video.sibnet.ru/shell.php?videoid=3232547"
        },
        comments=[],
        total_ratings=1000,
        average_rating=9.0,
        age_rating="R-17+",
        type="TV Сериал",
        next_episode_date=None,
        popularity_rank=1,
        views=1500000
    ),
    AnimeBase(
        id=2,
        title="Death Note",
        japanese_title="デスノート",
        description="Студент старшей школы находит сверхъестественную тетрадь смерти, которая позволяет ему убивать любого, чье имя он запишет в нее.",
        image_url="https://cdn.myanimelist.net/images/anime/9/9453.jpg",
        episodes=37,
        status="Завершён",
        genre=["Триллер", "Психологическое", "Сверхъестественное"],
        rating=8.7,
        studio="Madhouse",
        duration="23 мин",
        season="Осень 2006",
        video_sources={
            "1080p": "https://video.sibnet.ru/shell.php?videoid=3124444",
            "720p": "https://video.sibnet.ru/shell.php?videoid=3124444",
            "480p": "https://video.sibnet.ru/shell.php?videoid=3124444"
        },
        comments=[],
        total_ratings=950,
        average_rating=8.7,
        age_rating="R-17+",
        type="TV Сериал",
        next_episode_date=None,
        popularity_rank=2,
        views=1200000
    ),
    AnimeBase(
        id=3,
        title="One Punch Man",
        japanese_title="ワンパンマン",
        description="История о герое, который может победить любого противника одним ударом, но страдает от того, что не может найти достойного соперника.",
        image_url="https://cdn.myanimelist.net/images/anime/12/76049.jpg",
        episodes=12,
        status="Завершён",
        genre=["Экшен", "Комедия", "Супер сила"],
        rating=8.5,
        studio="Madhouse",
        duration="24 мин",
        season="Осень 2015",
        video_sources={
            "1080p": "https://video.sibnet.ru/shell.php?videoid=4521123",
            "720p": "https://video.sibnet.ru/shell.php?videoid=4521123",
            "480p": "https://video.sibnet.ru/shell.php?videoid=4521123"
        },
        comments=[],
        total_ratings=800,
        average_rating=8.5,
        age_rating="R-17+",
        type="TV Сериал",
        next_episode_date=None,
        popularity_rank=3,
        views=1000000
    )
]
