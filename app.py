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