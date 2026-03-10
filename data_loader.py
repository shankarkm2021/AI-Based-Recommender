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