// Глобальные переменные
let currentAnime = null;
let debounceTimer;
const API_URL = 'http://localhost:8000'; // Добавляем базовый URL API

// Функция для загрузки и отображения аниме
async function loadAnime() {
    const searchInput = document.getElementById('searchInput').value;
    const genreFilter = document.getElementById('genreFilter').value;
    const typeFilter = document.getElementById('typeFilter').value;
    const studioFilter = document.getElementById('studioFilter').value;
    const seasonFilter = document.getElementById('seasonFilter').value;
    const statusFilter = document.getElementById('statusFilter').value;
    const ageRatingFilter = document.getElementById('ageRatingFilter').value;
    const sortBy = document.getElementById('sortBy').value;

    try {
        const response = await fetch(`${API_URL}/api/anime?search=${searchInput}&genre=${genreFilter}&type=${typeFilter}&studio=${studioFilter}&season=${seasonFilter}&status=${statusFilter}&age_rating=${ageRatingFilter}&sort=${sortBy}`);
        const animeList = await response.json();
        
        const animeGrid = document.getElementById('animeGrid');
        animeGrid.innerHTML = '';

        animeList.forEach(anime => {
            const card = createAnimeCard(anime);
            animeGrid.appendChild(card);
        });

        // Обновляем фильтры, если это первая загрузка
        if (!genreFilter) {
            updateFilters(animeList);
        }
    } catch (error) {
        console.error('Error loading anime:', error);
        document.getElementById('animeGrid').innerHTML = '<div class="error">Ошибка загрузки данных</div>';
    }
}

// Создание карточки аниме
function createAnimeCard(anime) {
    const card = document.createElement('div');
    card.className = 'anime-card';
    card.onclick = () => showAnimeDetails(anime);

    card.innerHTML = `
        <img src="${anime.image_url}" alt="${anime.title}" loading="lazy">
        <div class="anime-info">
            <h3 class="anime-title">${anime.title}</h3>
            <div class="anime-japanese-title">${anime.japanese_title}</div>
            <div class="anime-details">
                <span class="anime-rating">${anime.average_rating.toFixed(1)}</span>
                <span>${anime.episodes} эп.</span>
                <span>${anime.status}</span>
            </div>
            <div class="anime-genres">
                ${anime.genre.slice(0, 3).map(genre => 
                    `<span class="genre-tag">${genre}</span>`
                ).join('')}
            </div>
        </div>
    `;

    return card;
}

// Обновление фильтров
function updateFilters(animeList) {
    const genres = new Set();
    const types = new Set();
    const studios = new Set();
    const seasons = new Set();
    const ageRatings = new Set();

    animeList.forEach(anime => {
        anime.genre.forEach(g => genres.add(g));
        types.add(anime.type);
        studios.add(anime.studio);
        seasons.add(anime.season);
        ageRatings.add(anime.age_rating);
    });

    updateFilterOptions('genreFilter', [...genres].sort());
    updateFilterOptions('typeFilter', [...types].sort());
    updateFilterOptions('studioFilter', [...studios].sort());
    updateFilterOptions('seasonFilter', [...seasons].sort());
    updateFilterOptions('ageRatingFilter', [...ageRatings].sort());
}

// Обновление опций фильтра
function updateFilterOptions(filterId, options) {
    const filter = document.getElementById(filterId);
    const currentValue = filter.value;

    filter.innerHTML = `<option value="">Все ${filter.options[0].text.toLowerCase()}</option>`;
    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.textContent = option;
        filter.appendChild(optionElement);
    });

    filter.value = currentValue;
}

// Отображение деталей аниме
async function showAnimeDetails(anime) {
    currentAnime = anime;
    
    const modal = document.getElementById('animeModal');
    const modalImage = document.getElementById('modalImage');
    const modalTitle = document.getElementById('modalTitle');
    const modalJapaneseTitle = document.getElementById('modalJapaneseTitle');
    const modalDescription = document.getElementById('modalDescription');
    const modalRating = document.getElementById('modalRating');
    const modalEpisodes = document.getElementById('modalEpisodes');
    const modalStatus = document.getElementById('modalStatus');
    const modalStudio = document.getElementById('modalStudio');
    const modalSeason = document.getElementById('modalSeason');
    const modalViews = document.getElementById('modalViews');
    const modalType = document.getElementById('modalType');
    const modalAgeRating = document.getElementById('modalAgeRating');
    const modalGenres = document.getElementById('modalGenres');

    modalImage.src = anime.image_url;
    modalTitle.textContent = anime.title;
    modalJapaneseTitle.textContent = anime.japanese_title;
    modalDescription.textContent = anime.description;
    modalRating.textContent = `Рейтинг: ${anime.average_rating.toFixed(1)} (${anime.total_ratings} оценок)`;
    modalEpisodes.textContent = `Эпизоды: ${anime.episodes}`;
    modalStatus.textContent = `Статус: ${anime.status}`;
    modalStudio.textContent = `Студия: ${anime.studio}`;
    modalSeason.textContent = `Сезон: ${anime.season}`;
    modalViews.textContent = `Просмотров: ${anime.views}`;
    modalType.textContent = `Тип: ${anime.type}`;
    modalAgeRating.textContent = `Возрастной рейтинг: ${anime.age_rating}`;
    
    modalGenres.innerHTML = anime.genre.map(genre => 
        `<span class="genre-tag">${genre}</span>`
    ).join('');

    // Загружаем комментарии
    await loadComments(anime.id);

    modal.style.display = 'block';
}

// Загрузка комментариев
async function loadComments(animeId) {
    try {
        const response = await fetch(`${API_URL}/api/anime/${animeId}/comments`);
        const comments = await response.json();
        
        const commentsList = document.getElementById('commentsList');
        commentsList.innerHTML = '';

        comments.forEach(comment => {
            const commentElement = document.createElement('div');
            commentElement.className = 'comment';
            commentElement.innerHTML = `
                <div class="comment-header">
                    <span class="comment-user">${comment.user_name}</span>
                    <span class="comment-rating">${comment.rating}/10</span>
                </div>
                <div class="comment-text">${comment.text}</div>
                <div class="comment-date">${new Date(comment.created_at).toLocaleDateString()}</div>
            `;
            commentsList.appendChild(commentElement);
        });
    } catch (error) {
        console.error('Error loading comments:', error);
    }
}

// Добавление комментария
async function addComment() {
    if (!currentAnime) return;

    const userName = document.getElementById('commentUserName').value;
    const commentText = document.getElementById('commentText').value;
    const rating = document.getElementById('commentRating').value;

    if (!userName || !commentText || !rating) {
        alert('Пожалуйста, заполните все поля');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/api/anime/${currentAnime.id}/comments`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_name: userName,
                text: commentText,
                rating: parseFloat(rating)
            })
        });

        if (response.ok) {
            // Очищаем поля
            document.getElementById('commentUserName').value = '';
            document.getElementById('commentText').value = '';
            document.getElementById('commentRating').value = '10';

            // Перезагружаем комментарии
            await loadComments(currentAnime.id);
            
            // Обновляем список аниме для отображения нового рейтинга
            await loadAnime();
        } else {
            alert('Ошибка при добавлении комментария');
        }
    } catch (error) {
        console.error('Error adding comment:', error);
        alert('Ошибка при добавлении комментария');
    }
}

// Просмотр аниме
function watchAnime() {
    if (!currentAnime || !currentAnime.video_sources) return;

    const watchModal = document.getElementById('watchModal');
    const videoPlayer = document.getElementById('videoPlayer');
    const qualitySelector = document.getElementById('videoQuality');
    
    // Обновляем список качества
    qualitySelector.innerHTML = '';
    Object.keys(currentAnime.video_sources).forEach(quality => {
        const option = document.createElement('option');
        option.value = quality;
        option.textContent = quality;
        qualitySelector.appendChild(option);
    });

    // Устанавливаем видео
    updateVideoSource();
    
    // Увеличиваем счетчик просмотров
    incrementViews();

    watchModal.style.display = 'block';
}

// Обновление источника видео
function updateVideoSource() {
    const quality = document.getElementById('videoQuality').value;
    const videoPlayer = document.getElementById('videoPlayer');
    
    if (currentAnime && currentAnime.video_sources && currentAnime.video_sources[quality]) {
        const videoUrl = currentAnime.video_sources[quality];
        
        // Для видео с Sibnet всегда используем iframe
        videoPlayer.innerHTML = `
            <iframe 
                width="100%" 
                height="500px" 
                src="${videoUrl}" 
                frameborder="0" 
                allowfullscreen 
                allow="autoplay; fullscreen">
            </iframe>
        `;
    }
}

// Увеличение счетчика просмотров
async function incrementViews() {
    if (!currentAnime) return;

    try {
        await fetch(`${API_URL}/api/anime/${currentAnime.id}/view`, {
            method: 'POST'
        });
    } catch (error) {
        console.error('Error incrementing views:', error);
    }
}

// Debounce функция для поиска
function debounceSearch() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(loadAnime, 300);
}

// Закрытие модальных окон
document.querySelectorAll('.close').forEach(closeBtn => {
    closeBtn.onclick = function() {
        this.closest('.modal').style.display = 'none';
        
        // Если закрываем окно просмотра, останавливаем видео
        if (this.closest('.watch-modal')) {
            const videoPlayer = document.getElementById('videoPlayer');
            videoPlayer.innerHTML = '';
        }
    }
});

// Обработка клика вне модального окна
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
        
        // Если закрываем окно просмотра, останавливаем видео
        if (event.target.classList.contains('watch-modal')) {
            const videoPlayer = document.getElementById('videoPlayer');
            videoPlayer.innerHTML = '';
        }
    }
}

// Кнопка просмотра
document.getElementById('watchButton').onclick = watchAnime;

// Изменение качества видео
document.getElementById('videoQuality').onchange = updateVideoSource;

// Загрузка аниме при загрузке страницы
document.addEventListener('DOMContentLoaded', loadAnime);
