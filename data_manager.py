from flask import Flask
from models import db, User, Movie
from data_manager_interface import DataManagerInterface

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app: Flask):
        db.init_app(app)
        with app.app_context():
            db.create_all()

    def get_all_users(self):
        return User.query.all()

    def get_user(self, user_id):
        return User.query.get(user_id)

    def add_user(self, user_data):
        user = User(name=user_data['name'])
        db.session.add(user)
        db.session.commit()
        return user

    def get_user_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, user_id, movie_data):
        movie = Movie(user_id=user_id, **movie_data)
        db.sessio.add(movie)
        db.session.commit()
        return movie

    def update_movie(self, user_id, movie_id, movie_data):
        movie = Movie.query.filter_by(id=movie_id, user_id=user_id).first()
        if movie:
            for key, value in movie_data.items():
                setattr(movie, key, value)
            db.session.commit()
        return movie

    def delete_movie(self, user_id, movie_id):
        movie = Movie.query.filter_by(id=movie_id, user_id=user_id).first()
        if movie:
            db.session.delete(movie)
            db.session.commit()
        return movie
