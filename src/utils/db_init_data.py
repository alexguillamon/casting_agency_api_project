from database.models import db, Movie, Actor
from utils.seed_data import movies_data, actors_data


def seed():
    # Add seed data to the database.
    actors_list = []
    for actor_data in actors_data:
        name, DOB, gender = actor_data.values()
        new_actor = Actor(name=name, DOB=DOB, gender=gender)
        actors_list.append(new_actor)

    movies_list = []
    for i, movie_data in enumerate(movies_data):
        title, release_date = movie_data.values()
        new_movie = Movie(title=title, release_date=release_date)
        new_movie.cast.append(actors_list[i])
        movies_list.append(new_movie)

    db.session.add_all(actors_list)
    db.session.add_all(movies_list)
    db.session.commit()
    db.session.close()
