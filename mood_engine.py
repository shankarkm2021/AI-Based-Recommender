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