// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// DOM Elements
const moodInput = document.getElementById('moodInput');
const recommendBtn = document.getElementById('recommendBtn');
const moodPills = document.querySelectorAll('.pill');
const loadingIndicator = document.getElementById('loadingIndicator');
const recommendationsSection = document.getElementById('recommendationsSection');
const recommendationsGrid = document.getElementById('recommendationsGrid');
const moodSummary = document.getElementById('moodSummary');
const errorMessage = document.getElementById('errorMessage');

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Load mood keywords
    fetchMoodKeywords();
});

recommendBtn.addEventListener('click', getRecommendations);

moodInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        getRecommendations();
    }
});

moodPills.forEach(pill => {
    pill.addEventListener('click', () => {
        const mood = pill.dataset.mood;
        moodInput.value = `I feel ${mood} and want something ${getMoodDescription(mood)}`;
        getRecommendations();
    });
});

// Helper Functions
function getMoodDescription(mood) {
    const descriptions = {
        'happy': 'fun and uplifting',
        'sad': 'emotional and touching',
        'adventurous': 'exciting and thrilling',
        'romantic': 'sweet and romantic',
        'scared': 'spooky but entertaining',
        'thoughtful': 'deep and thought-provoking',
        'energetic': 'fast-paced and dynamic',
        'relaxed': 'calm and peaceful'
    };
    return descriptions[mood] || 'entertaining';
}

async function fetchMoodKeywords() {
    try {
        const response = await fetch(`${API_BASE_URL}/mood/keywords`);
        const data = await response.json();
        if (data.success) {
            console.log('Mood keywords loaded:', data.keywords);
        }
    } catch (error) {
        console.error('Error loading mood keywords:', error);
    }
}

async function getRecommendations() {
    const mood = moodInput.value.trim();
    
    if (!mood) {
        showError('Please tell us how you\'re feeling!');
        return;
    }
    
    // Show loading, hide previous results
    showLoading();
    hideError();
    
    try {
        const response = await fetch(`${API_BASE_URL}/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ mood })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayRecommendations(data);
        } else {
            showError(data.error || 'Something went wrong');
        }
    } catch (error) {
        showError('Network error. Please check if the server is running.');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

function displayRecommendations(data) {
    const { recommendations, input_mood } = data;
    
    if (recommendations.length === 0) {
        showError('No movies found matching your mood. Try a different description!');
        return;
    }
    
    // Update mood summary
    moodSummary.textContent = `Based on: "${input_mood}"`;
    
    // Clear grid
    recommendationsGrid.innerHTML = '';
    
    // Create movie cards
    recommendations.forEach(movie => {
        const card = createMovieCard(movie);
        recommendationsGrid.appendChild(card);
    });
    
    // Show section
    recommendationsSection.classList.remove('hidden');
    
    // Scroll to recommendations
    recommendationsSection.scrollIntoView({ behavior: 'smooth' });
}

function createMovieCard(movie) {
    const card = document.createElement('div');
    card.className = 'movie-card';
    
    // Get emoji based on genre
    const genreEmoji = getGenreEmoji(movie.genre);
    
    card.innerHTML = `
        <div class="movie-poster">${genreEmoji}</div>
        <div class="movie-info">
            <h3>${movie.title}</h3>
            <div class="movie-meta">
                <span>${movie.year}</span>
                <span>${movie.genre}</span>
            </div>
            <p class="movie-description">${movie.description}</p>
            <div class="movie-footer">
                <span class="movie-rating">⭐ ${movie.rating}</span>
                <span class="match-score">${movie.similarity_score}% Match</span>
            </div>
            <div class="movie-moods">
                ${movie.matched_mood.map(m => `<span class="mood-tag">#${m}</span>`).join('')}
            </div>
        </div>
    `;
    
    // Add click handler
    card.addEventListener('click', () => {
        alert(`You selected: ${movie.title}\n\nThis movie is a ${movie.similarity_score}% match for your mood!`);
    });
    
    return card;
}

function getGenreEmoji(genre) {
    const emojiMap = {
        'Comedy': '😂',
        'Drama': '🎭',
        'Action': '💥',
        'Adventure': '🗺️',
        'Romance': '💕',
        'Horror': '👻',
        'Thriller': '🔪',
        'Documentary': '📚',
        'Nature': '🌿',
        'Sports': '⚽',
        'default': '🎬'
    };
    
    for (const [key, emoji] of Object.entries(emojiMap)) {
        if (genre.includes(key)) {
            return emoji;
        }
    }
    return emojiMap.default;
}

function showLoading() {
    loadingIndicator.classList.remove('hidden');
    recommendationsSection.classList.add('hidden');
}

function hideLoading() {
    loadingIndicator.classList.add('hidden');
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
    recommendationsSection.classList.add('hidden');
}

function hideError() {
    errorMessage.classList.add('hidden');
}