from flask import Flask, request, jsonify
from data_manager import SQLiteDataManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

data_manager = SQLiteDataManager(app)


# helper function movie serialization
def serialize_movie(movie):
    return {
        'movie_id': movie.id,
        'title': movie.title,
        'release_year': movie.release_year,
        'genre': movie.genre,
        'director': movie.director,
        'rating': movie.rating,
        'user_id': movie.user.id

    }

# helper function user serialization
def serialize_user(user):
    return {
        'id': user.id,
        'name': user.name
    }

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        db_users = data_manager.get_all_users()
        user_list = []
        for user in db_users:
            serialize = serialize_user(user)
            user_list.append(serialize)
        return jsonify(user_list)
    elif request.method == 'POST':
        data = request.get_json()
        user = data_manager.add_user(data)
        serialized = serialize_user(user)
        return jsonify(serialized)

@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def user_movies(user_id):
    if request.method == 'GET':
        movies = data_manager.get_user_movies(user_id)
        movie_list = []
        for movie in movies:
            serialized = serialize_movie(movie)
            movie_list.append(serialized)
        return jsonify(movie_list)

    elif request.method == 'POST':
        data = request.get_json()
        movie = data_manager.add_movie(user_id, data)
        serialize = serialize_movie(movie)
        return jsonify(serialize)

@app.route('/users/<int:user_id>/movies/<int:movie_id>', methods=['PUT', 'DELETE'])
def movie_detail(user_id, movie_id):
    if request.method == 'PUT':
        data = request.get_json()
        movie = data_manager.update_movie(user_id, movie_id, data)
        serialize = serialize_movie(movie)
        return jsonify(serialize)

    elif request.method == 'DELETE':
        data_manager.delete_movie(user_id, movie_id)
        return jsonify({'message': f"Movie {movie_id} deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)

