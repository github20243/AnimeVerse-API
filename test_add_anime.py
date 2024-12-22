import requests
from datetime import date

# Список тестовых аниме
test_anime_list = [
    {
        "title": "Demon Slayer: Kimetsu no Yaiba",
        "japanese_title": "鬼滅の刃",
        "description": "В мире, где демоны питаются людьми и существуют веками, юный Танджиро Камадо становится охотником на демонов после того, как его семья была убита, а младшая сестра Незуко превращена в демона.",
        "video_url": "https://example.com/demon-slayer-episode-1",
        "thumbnail_url": "https://example.com/demon-slayer-thumbnail.jpg",
        "release_date": str(date(2019, 4, 6)),
        "episodes": 26,
        "status": "Completed",
        "genre": ["Action", "Fantasy", "Adventure", "Supernatural"],
        "rating": 8.9,
        "studio": "ufotable",
        "duration": "23 min per ep",
        "season": "Spring 2019"
    },
    {
        "title": "Attack on Titan",
        "japanese_title": "進撃の巨人",
        "description": "Человечество живет внутри городов, окруженных огромными стенами, которые защищают их от таинственных гигантов, пожирающих людей.",
        "video_url": "https://example.com/attack-on-titan-episode-1",
        "thumbnail_url": "https://example.com/attack-on-titan-thumbnail.jpg",
        "release_date": str(date(2013, 4, 7)),
        "episodes": 25,
        "status": "Completed",
        "genre": ["Action", "Drama", "Fantasy", "Mystery"],
        "rating": 9.0,
        "studio": "Wit Studio",
        "duration": "24 min per ep",
        "season": "Spring 2013"
    },
    {
        "title": "My Hero Academia",
        "japanese_title": "僕のヒーローアカデミア",
        "description": "В мире, где 80% населения обладает сверхспособностями, родился Идзуку Мидория — один из немногих людей, у которых таких способностей нет.",
        "video_url": "https://example.com/my-hero-academia-episode-1",
        "thumbnail_url": "https://example.com/my-hero-academia-thumbnail.jpg",
        "release_date": str(date(2016, 4, 3)),
        "episodes": 13,
        "status": "Ongoing",
        "genre": ["Action", "Comedy", "Supernatural"],
        "rating": 8.5,
        "studio": "Bones",
        "duration": "23 min per ep",
        "season": "Spring 2016"
    }
]

def test_api():
    base_url = "http://localhost:8000"
    
    # Добавляем аниме
    print("Добавляем тестовые аниме...")
    for anime in test_anime_list:
        response = requests.post(f"{base_url}/api/anime", json=anime)
        if response.status_code == 200:
            print(f"Успешно добавлено аниме: {anime['title']}")
        else:
            print(f"Ошибка при добавлении аниме {anime['title']}: {response.status_code}")
    
    # Тестируем поиск
    print("\nТестируем поиск...")
    search_response = requests.get(f"{base_url}/api/search", params={"query": "demon"})
    if search_response.status_code == 200:
        results = search_response.json()
        print(f"Найдено аниме по запросу 'demon': {len(results)}")
        for anime in results:
            print(f"- {anime['title']}")
    
    # Тестируем фильтрацию по жанру
    print("\nТестируем фильтрацию по жанру...")
    filter_response = requests.get(f"{base_url}/api/anime", params={"genre": "Action"})
    if filter_response.status_code == 200:
        results = filter_response.json()
        print(f"Найдено аниме жанра 'Action': {len(results)}")
        for anime in results:
            print(f"- {anime['title']}")
    
    # Тестируем сортировку по рейтингу
    print("\nТестируем сортировку по рейтингу...")
    sort_response = requests.get(f"{base_url}/api/anime", params={"sort_by": "rating", "sort_order": "desc"})
    if sort_response.status_code == 200:
        results = sort_response.json()
        print("Аниме отсортированные по рейтингу (по убыванию):")
        for anime in results:
            print(f"- {anime['title']}: {anime['rating']}")

if __name__ == "__main__":
    test_api()
