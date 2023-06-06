#!/usr/bin/env python3
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ipdb;

from models import Role, Movie, Actor


if __name__ == '__main__':
    
    engine = create_engine('sqlite:///db/movies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Test the Object Relationship Methods
    role = session.query(Role).first()
    if role and role.get_actor():
        print("Role Actor: ", role.get_actor().name)
    else:
        print("No role found.")
    print()

    movie = session.query(Movie).first()
    print("Movie Roles: ", [r.character_name for r in movie.get_roles()])
    print("Movie Actors: ", [a.name for a in movie.get_actors()])
    print()

    actor = session.query(Actor).first()
    print("Actor Roles: ", [r.character_name for r in actor.get_roles()])
    print("Actor Movies: ", [m.title for m in actor.get_movies()])
    print()

    # Test the Aggregate and Relationship Methods
    print("Role Credit: ", role.credit())
    print()

    movie.cast_role(actor, "New Character", 5000000)
    print("Movie All Credits: ", movie.all_credits())
    print()

    movie.fire_actor(actor)
    print("Movie All Credits after firing actor: ", movie.all_credits())
    print()

    print("Actor Total Salary: ", actor.total_salary())
    print("Actor Blockbusters: ", [movie.title for movie in actor.blockbusters()])
    print()

    most_successful_actor = Actor.most_successful(session)
    print("Most Successful Actor: ", most_successful_actor.name)

    # Close the session
    session.close()

    ipdb.set_trace()
