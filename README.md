# Anime Site Backend

Бэкенд для сайта с аниме, написанный на FastAPI.

## Особенности

- Каталог аниме с подробной информацией
- Система комментариев и рейтингов
- Встроенный видеоплеер с поддержкой разных источников
- API для фильтрации и поиска аниме
- Поддержка сортировки по различным параметрам

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/anime-site-backend.git
cd anime-site-backend
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите сервер:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /api/anime` - Получить список аниме с фильтрами
- `GET /api/anime/{anime_id}` - Получить информацию об определенном аниме
- `GET /api/anime/{anime_id}/comments` - Получить комментарии к аниме
- `POST /api/anime/{anime_id}/comments` - Добавить комментарий
- `POST /api/anime/{anime_id}/view` - Увеличить счетчик просмотров

## Структура проекта

```
anime-site-backend/
├── app/
│   ├── api/
│   ├── models/
│   ├── services/
│   └── utils/
├── static/
│   ├── css/
│   └── js/
├── main.py
├── anime_data.py
├── requirements.txt
└── README.md
```

## Технологии

- FastAPI
- Pydantic
- Uvicorn
- Python 3.8+

## Лицензия

MIT
