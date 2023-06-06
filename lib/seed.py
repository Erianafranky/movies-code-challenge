
from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Role, Movie, Actor

if __name__ == '__main__':
    engine = create_engine('sqlite:///db/movies.db')
    Session = sessionmaker(bind=engine)
    session = Session()
   
    session.query(Role).delete()
    session.query(Actor).delete()
    session.query(Movie).delete()

    print("Seeding roles...")

    # Create actors
    actors = []
    for i in range(1, 5001):
        actor = Actor(name=f"Actor {i}")
        actors.append(actor)
        session.add(actor)

    # Create movies
    movies = []
    for i in range(1, 5001):
        movie = Movie(title=f"Movie {i}", box_office_earnings=i * 1000000)
        movies.append(movie)
        session.add(movie)

    # Create roles
    for i in range(1, 5001):
        role = Role(
            character_name=f"Character {i}",
            salary=i * 1000,
            movie=movies[i - 1],
            actor=actors[i - 1]
        )
        session.add(role)

    # Commit the session
    session.commit()


    
    