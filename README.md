PROJECT 1: MoodSense - AI Mood-Based Recommender
📁 Complete Repository Structure
Create this folder structure on your local machine:

text
moodsense-recommender/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── mood_engine.py
│   ├── data_loader.py
│   └── config.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── assets/
├── data/
│   └── sample_movies.json
├── .gitignore
├── README.md
└── LICENSE
📝 Complete Code Files
1. backend/requirements.txt
txt
flask==2.3.3
flask-cors==4.0.0
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
nltk==3.8.1
gunicorn==21.2.0
python-dotenv==1.0.0
2. backend/config.py
python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = os.getenv('DEBUG', True)
    PORT = int(os.getenv('PORT', 5000))
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DATA_FILE = os.getenv('DATA_FILE', 'data/sample_movies.json')
3. backend/mood_engine.py
python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

class MoodEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            lowercase=True
        )
        self.movies = []
        self.movie_vectors = None
        self.mood_keywords = {
            'happy': ['joy', 'fun', 'comedy', 'laugh', 'bright', 'cheerful', 'upbeat', 'celebration'],
            'sad': ['emotional', 'touching', 'heartfelt', 'poignant', 'bittersweet', 'melancholy'],
            'adventurous': ['action', 'journey', 'explore', 'quest', 'adventure', 'epic', 'thrilling'],
            'romantic': ['love', 'romance', 'heart', 'couple', 'dating', 'relationship', 'passion'],
            'scared': ['horror', 'thriller', 'creepy', 'suspense', 'spooky', 'dark', 'mystery'],
            'thoughtful': ['documentary', 'biography', 'history', 'science', 'philosophy', 'deep'],
            'energetic': ['sports', 'race', 'competition', 'fast', 'intense', 'pulse', 'adrenaline'],
            'relaxed': ['peaceful', 'calm', 'nature', 'slow', 'gentle', 'soothing', 'meditation']
        }
        
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
        return ' '.join(tokens)
    
    def load_movies(self, movies_data):
        """Load and preprocess movies"""
        self.movies = movies_data
        # Create combined text features
        combined_texts = []
        for movie in movies_data:
            text = f"{movie['title']} {movie['genre']} {movie['description']} {movie.get('keywords', '')}"
            processed = self.preprocess_text(text)
            combined_texts.append(processed)
        
        # Vectorize
        self.movie_vectors = self.vectorizer.fit_transform(combined_texts)
        return len(self.movies)
    
    def analyze_mood(self, user_input):
        """Convert user mood input to search vector"""
        processed_input = self.preprocess_text(user_input)
        
        # Extract mood keywords
        mood_words = []
        input_lower = user_input.lower()
        
        for mood, keywords in self.mood_keywords.items():
            if any(keyword in input_lower for keyword in keywords):
                mood_words.extend(keywords)
        
        # Combine with processed input
        search_text = processed_input + ' ' + ' '.join(mood_words)
        search_vector = self.vectorizer.transform([search_text])
        
        return search_vector, mood_words
    
    def get_recommendations(self, user_input, top_n=5):
        """Get movie recommendations based on mood"""
        if not self.movies or self.movie_vectors is None:
            return []
        
        search_vector, mood_keywords = self.analyze_mood(user_input)
        
        # Calculate similarities
        similarities = cosine_similarity(search_vector, self.movie_vectors).flatten()
        
        # Get top indices
        top_indices = similarities.argsort()[-top_n:][::-1]
        
        # Prepare recommendations
        recommendations = []
        for idx in top_indices:
            if similarities[idx] > 0.01:  # Threshold
                movie = self.movies[idx].copy()
                movie['similarity_score'] = round(float(similarities[idx]) * 100, 2)
                movie['matched_mood'] = mood_keywords[:3] if mood_keywords else ['general']
                recommendations.append(movie)
        
        return recommendations
    
    def add_movie(self, movie_data):
        """Add a new movie to the database"""
        self.movies.append(movie_data)
        # Rebuild vectors
        combined_texts = []
        for movie in self.movies:
            text = f"{movie['title']} {movie['genre']} {movie['description']}"
            processed = self.preprocess_text(text)
            combined_texts.append(processed)
        
        self.movie_vectors = self.vectorizer.fit_transform(combined_texts)
        return True
4. backend/data_loader.py
python
import json
import os

class DataLoader:
    @staticmethod
    def load_sample_data():
        """Generate sample movie data"""
        return [
            {
                "id": 1,
                "title": "The Joyful Journey",
                "genre": "Comedy/Adventure",
                "description": "A heartwarming tale of friends discovering happiness on a road trip",
                "year": 2023,
                "rating": 4.5,
                "poster": "🎭",
                "keywords": "funny happy adventure friends travel"
            },
            {
                "id": 2,
                "title": "Midnight Whispers",
                "genre": "Drama/Romance",
                "description": "A touching story about love found in unexpected places",
                "year": 2022,
                "rating": 4.2,
                "poster": "💕",
                "keywords": "romantic emotional love relationship"
            },
            {
                "id": 3,
                "title": "Mountain Quest",
                "genre": "Action/Adventure",
                "description": "Thrilling expedition to conquer the world's highest peak",
                "year": 2023,
                "rating": 4.8,
                "poster": "⛰️",
                "keywords": "adventure action climb mountain thrilling"
            },
            {
                "id": 4,
                "title": "Science Unveiled",
                "genre": "Documentary",
                "description": "Exploring the mysteries of the universe with leading scientists",
                "year": 2021,
                "rating": 4.6,
                "poster": "🔬",
                "keywords": "documentary science educational thought-provoking"
            },
            {
                "id": 5,
                "title": "Laughter Club",
                "genre": "Comedy",
                "description": "A group of strangers find humor in everyday situations",
                "year": 2023,
                "rating": 4.3,
                "poster": "😂",
                "keywords": "comedy funny laugh humorous lighthearted"
            },
            {
                "id": 6,
                "title": "Shadow Realm",
                "genre": "Horror/Thriller",
                "description": "A family moves into a house with a dark secret",
                "year": 2022,
                "rating": 4.1,
                "poster": "👻",
                "keywords": "horror scary thriller suspense creepy"
            },
            {
                "id": 7,
                "title": "Ocean Calm",
                "genre": "Documentary/Nature",
                "description": "Breathtaking footage of marine life and peaceful underwater worlds",
                "year": 2023,
                "rating": 4.7,
                "poster": "🌊",
                "keywords": "nature calm peaceful relaxing ocean"
            },
            {
                "id": 8,
                "title": "Speed Demons",
                "genre": "Action/Sports",
                "description": "High-octane racing film about rival drivers",
                "year": 2022,
                "rating": 4.4,
                "poster": "🏎️",
                "keywords": "racing fast action sports energetic adrenaline"
            }
        ]
    
    @staticmethod
    def save_to_file(data, filename):
        """Save data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def load_from_file(filename):
        """Load data from JSON file"""
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return None
5. backend/app.py
python
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from mood_engine import MoodEngine
from data_loader import DataLoader
from config import Config
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Initialize engine and load data
mood_engine = MoodEngine()
data_loader = DataLoader()

# Load or create sample data
movies = data_loader.load_sample_data()
mood_engine.load_movies(movies)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    """Get movie recommendations based on mood"""
    try:
        data = request.json
        user_input = data.get('mood', '')
        
        if not user_input:
            return jsonify({'error': 'No mood input provided'}), 400
        
        recommendations = mood_engine.get_recommendations(user_input, top_n=6)
        
        return jsonify({
            'success': True,
            'input_mood': user_input,
            'recommendations': recommendations,
            'count': len(recommendations)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/movies', methods=['GET'])
def get_all_movies():
    """Get all movies"""
    return jsonify({
        'success': True,
        'movies': movies,
        'count': len(movies)
    })

@app.route('/api/movies', methods=['POST'])
def add_movie():
    """Add a new movie"""
    try:
        movie_data = request.json
        required_fields = ['title', 'genre', 'description']
        
        for field in required_fields:
            if field not in movie_data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Generate new ID
        new_id = max([m['id'] for m in movies]) + 1
        movie_data['id'] = new_id
        movie_data['poster'] = movie_data.get('poster', '🎬')
        movie_data['rating'] = float(movie_data.get('rating', 0))
        movie_data['year'] = int(movie_data.get('year', 2024))
        
        # Add to engine
        movies.append(movie_data)
        mood_engine.add_movie(movie_data)
        
        return jsonify({
            'success': True,
            'movie': movie_data,
            'message': 'Movie added successfully'
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mood/keywords', methods=['GET'])
def get_mood_keywords():
    """Get available mood keywords"""
    return jsonify({
        'success': True,
        'keywords': mood_engine.mood_keywords
    })

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
6. frontend/index.html
html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MoodSense - AI Movie Recommender</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <div class="app-container">
        <!-- Header -->
        <header class="header">
            <div class="logo">
                <span class="logo-icon">🎭</span>
                <h1>MoodSense</h1>
            </div>
            <p class="tagline">Movies that match your mood</p>
        </header>

        <!-- Main Content -->
        <main class="main-content">
            <!-- Mood Input Section -->
            <section class="mood-section">
                <h2>How are you feeling today?</h2>
                <div class="input-container">
                    <textarea 
                        id="moodInput" 
                        placeholder="e.g., I feel adventurous and want something exciting... or I need a good laugh after a long day..."
                        rows="3"
                    ></textarea>
                    <button id="recommendBtn" class="primary-btn">
                        <span>Find Movies</span>
                        <span class="btn-icon">→</span>
                    </button>
                </div>
                
                <!-- Quick Mood Pills -->
                <div class="mood-pills">
                    <button class="pill" data-mood="happy">😊 Happy</button>
                    <button class="pill" data-mood="sad">😢 Sad</button>
                    <button class="pill" data-mood="adventurous">🗺️ Adventurous</button>
                    <button class="pill" data-mood="romantic">💕 Romantic</button>
                    <button class="pill" data-mood="scared">😨 Scared</button>
                    <button class="pill" data-mood="thoughtful">🤔 Thoughtful</button>
                    <button class="pill" data-mood="energetic">⚡ Energetic</button>
                    <button class="pill" data-mood="relaxed">😌 Relaxed</button>
                </div>
            </section>

            <!-- Loading Indicator -->
            <div id="loadingIndicator" class="loading hidden">
                <div class="spinner"></div>
                <p>Finding movies that match your mood...</p>
            </div>

            <!-- Recommendations Section -->
            <section id="recommendationsSection" class="recommendations-section hidden">
                <div class="section-header">
                    <h2>Your Personalized Recommendations</h2>
                    <p id="moodSummary" class="mood-summary"></p>
                </div>
                
                <div id="recommendationsGrid" class="recommendations-grid">
                    <!-- Movies will be inserted here -->
                </div>
            </section>

            <!-- Error Section -->
            <div id="errorMessage" class="error-message hidden"></div>
        </main>

        <!-- Footer -->
        <footer class="footer">
            <p>© 2024 MoodSense - Find your perfect movie match</p>
        </footer>
    </div>

    <script src="script.js"></script>
</body>
</html>
7. frontend/style.css
css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary-color: #6c5ce7;
    --secondary-color: #a29bfe;
    --background: #0f0f1a;
    --surface: #1a1a2e;
    --text-primary: #ffffff;
    --text-secondary: #b8b8d0;
    --accent: #00cec9;
    --error: #ff7675;
    --success: #55efc4;
}

body {
    font-family: 'Inter', sans-serif;
    background: var(--background);
    color: var(--text-primary);
    line-height: 1.6;
    min-height: 100vh;
}

.app-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

/* Header Styles */
.header {
    text-align: center;
    margin-bottom: 3rem;
}

.logo {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 0.5rem;
}

.logo-icon {
    font-size: 3rem;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.header h1 {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--primary-color), var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.tagline {
    color: var(--text-secondary);
    font-size: 1.2rem;
}

/* Mood Input Section */
.mood-section {
    background: var(--surface);
    border-radius: 1.5rem;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.mood-section h2 {
    margin-bottom: 1.5rem;
    font-size: 1.8rem;
}

.input-container {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}

textarea {
    flex: 1;
    padding: 1.2rem;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid transparent;
    border-radius: 1rem;
    color: var(--text-primary);
    font-size: 1rem;
    font-family: inherit;
    resize: vertical;
    transition: all 0.3s ease;
}

textarea:focus {
    outline: none;
    border-color: var(--primary-color);
    background: rgba(255, 255, 255, 0.1);
}

textarea::placeholder {
    color: var(--text-secondary);
}

.primary-btn {
    padding: 1.2rem 2rem;
    background: linear-gradient(135deg, var(--primary-color), var(--accent));
    border: none;
    border-radius: 1rem;
    color: white;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.primary-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(108, 92, 231, 0.3);
}

.btn-icon {
    font-size: 1.2rem;
}

/* Mood Pills */
.mood-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.8rem;
    justify-content: center;
}

.pill {
    padding: 0.6rem 1.2rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 2rem;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.9rem;
}

.pill:hover {
    background: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
    transform: scale(1.05);
}

/* Loading Indicator */
.loading {
    text-align: center;
    padding: 3rem;
}

.spinner {
    width: 50px;
    height: 50px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top-color: var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 1rem;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.hidden {
    display: none !important;
}

/* Recommendations Grid */
.recommendations-section {
    margin-top: 3rem;
}

.section-header {
    margin-bottom: 2rem;
}

.section-header h2 {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

.mood-summary {
    color: var(--text-secondary);
    font-style: italic;
}

.recommendations-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
}

.movie-card {
    background: var(--surface);
    border-radius: 1.2rem;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
    position: relative;
}

.movie-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

.movie-poster {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    padding: 2rem;
    text-align: center;
    font-size: 4rem;
}

.movie-info {
    padding: 1.5rem;
}

.movie-info h3 {
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
}

.movie-meta {
    display: flex;
    gap: 1rem;
    color: var(--text-secondary);
    font-size: 0.9rem;
    margin-bottom: 0.8rem;
}

.movie-description {
    color: var(--text-secondary);
    margin-bottom: 1rem;
    font-size: 0.95rem;
    line-height: 1.5;
}

.movie-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
}

.movie-rating {
    background: var(--accent);
    padding: 0.3rem 0.8rem;
    border-radius: 1rem;
    font-size: 0.9rem;
    font-weight: 600;
}

.match-score {
    background: rgba(108, 92, 231, 0.2);
    padding: 0.3rem 0.8rem;
    border-radius: 1rem;
    font-size: 0.9rem;
    color: var(--primary-color);
    font-weight: 600;
}

.movie-moods {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}

.mood-tag {
    background: rgba(255, 255, 255, 0.05);
    padding: 0.2rem 0.6rem;
    border-radius: 1rem;
    font-size: 0.8rem;
    color: var(--text-secondary);
}

/* Error Message */
.error-message {
    background: rgba(255, 118, 117, 0.1);
    border: 1px solid var(--error);
    color: var(--error);
    padding: 1rem;
    border-radius: 0.8rem;
    margin-top: 1rem;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 4rem;
    color: var(--text-secondary);
    font-size: 0.9rem;
}

/* Responsive Design */
@media (max-width: 768px) {
    .app-container {
        padding: 1rem;
    }
    
    .header h1 {
        font-size: 2rem;
    }
    
    .input-container {
        flex-direction: column;
    }
    
    .primary-btn {
        width: 100%;
        justify-content: center;
    }
    
    .recommendations-grid {
        grid-template-columns: 1fr;
    }
}
8. frontend/script.js
javascript
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
9. data/sample_movies.json
json
{
  "movies": [
    {
      "id": 1,
      "title": "The Joyful Journey",
      "genre": "Comedy/Adventure",
      "description": "A heartwarming tale of friends discovering happiness on a road trip",
      "year": 2023,
      "rating": 4.5,
      "poster": "🎭",
      "keywords": "funny happy adventure friends travel"
    },
    {
      "id": 2,
      "title": "Midnight Whispers",
      "genre": "Drama/Romance",
      "description": "A touching story about love found in unexpected places",
      "year": 2022,
      "rating": 4.2,
      "poster": "💕",
      "keywords": "romantic emotional love relationship"
    }
  ]
}
10. .gitignore
text
# Python
__pycache__/
*.py[cod]
*.so
.Python
env/
venv/
.env
*.egg-info/
dist/
build/

# Frontend
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Data (optional - if you want to exclude user data)
data/user_*.json
11. README.md
markdown
# 🎭 MoodSense - AI-Powered Movie Recommender

MoodSense is an intelligent movie recommendation system that suggests films based on your current emotional state. Simply describe how you're feeling, and our AI engine finds the perfect matches!

## ✨ Features

- **Natural Language Input**: Type how you feel in your own words
- **Smart Mood Detection**: AI analyzes your text to understand emotional context
- **Personalized Recommendations**: Movies matched to your specific mood
- **Quick Mood Pills**: One-click mood selections for instant recommendations
- **Visual Feedback**: See why each movie matches your mood

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Modern web browser

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/moodsense-recommender.git
cd moodsense-recommender
Install backend dependencies

bash
cd backend
pip install -r requirements.txt
Run the application

bash
python app.py
Open your browser
Navigate to http://localhost:5000

🎯 How It Works
User Input: Enter how you're feeling (e.g., "I feel adventurous and want something exciting")

Text Processing: Our engine cleans and analyzes your text

Mood Mapping: Keywords are extracted and mapped to mood categories

Similarity Search: TF-IDF vectorization finds movies with matching descriptions

Results: Top matches are returned with similarity scores

🏗️ Architecture
text
Frontend (HTML/CSS/JS) → Backend (Flask) → Mood Engine → Movie Database
         ↑                    ↑                 ↑
    User Interface       REST API         ML Processing
📊 Sample Moods
Mood	Keywords	Example Movies
😊 Happy	joy, fun, comedy	Comedies, Feel-good films
😢 Sad	emotional, touching	Dramas, Heartfelt stories
🗺️ Adventurous	action, journey	Adventure, Action films
💕 Romantic	love, romance	Romantic comedies, Love stories
🛠️ Technologies Used
Backend: Python, Flask, scikit-learn, NLTK

Frontend: HTML5, CSS3, JavaScript

ML: TF-IDF Vectorization, Cosine Similarity

Deployment: Gunicorn (production ready)

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Inspired by the need for emotion-based content discovery

Built with love for movie enthusiasts everywhere

text

### **12. LICENSE** (MIT License)
```txt
MIT
