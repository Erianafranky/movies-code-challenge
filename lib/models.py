import os
import sys
#from seed import session

sys.path.append(os.getcwd)

from sqlalchemy import (create_engine, PrimaryKeyConstraint, Column, String, Integer, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    salary = Column(Integer)
    character_name = Column(String)

    movie_id = Column(Integer, ForeignKey('movies.id'))
    actor_id = Column(Integer, ForeignKey('actors.id'))

    movie = relationship("Movie", back_populates="roles")
    actor = relationship("Actor", back_populates="roles")

    #return the actor instance 
    def get_actor(self):
        return self.actor

    #return the movie instance
    def get_movie(self):
        return self.movie
    
    #return a string with character name and actor name
    def credit(self):
        actor_name = self.actor.name if self.actor else "Unknown Actor"
        return f"{self.character_name}: Played by {actor_name}"


class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    roles = relationship('Role', back_populates='actor')

    #return a collection of all roles the actor played
    def get_roles(self):
        return self.roles

    #return a collection of all movies the actor has performed in
    def get_movies(self):
        return [role.movie for role in self.roles]

    #return a salary of an actor 
    def total_salary(self):
        return sum(role.salary for role in self.roles)

    #return a collection of all movie instances the actor has performed in
    def blockbusters(self):
        return [role.movie for role in self.roles if role.movie and role.movie.box_office_earnings > 50000000]
    
    #return an actor instance for the actor with highest salary
    @classmethod
    def most_successful(cls, session):
        actors = session.query(cls).all()
        return max(actors, key=lambda actor: actor.total_salary())

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String())
    box_office_earnings = Column(Integer())

    roles = relationship('Role', back_populates='movie')

    #returns a collection for all roles of the movie
    def get_roles(self):
        return self.roles

    #returns a collection of actors who performed in the movie
    def get_actors(self):
        return [role.actor for role in self.roles]

    #creates a new role in the db associated with the movie and actor
    def cast_role(self, actor, character_name, salary):
        role = Role(actor=actor, character_name=character_name, salary=salary)
        self.roles.append(role)

    #return an array of string with all the roles for the movie   
    def all_credits(self):
        return [role.credit() for role in self.roles]

    #takes an actor and remove their role from the movie
    def fire_actor(self, actor):
        role_to_delete = next((role for role in self.roles if role.actor == actor), None)
        if role_to_delete:
            self.roles.remove(role_to_delete)


