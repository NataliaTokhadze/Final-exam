from flask import Flask, redirect, url_for, render_template, request, session as flask_session
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import re
import bcrypt  # Import bcrypt

from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

Base = declarative_base()


class Anime(Base):
    __tablename__ = 'anime'
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    director = Column(String(40), nullable=False)
    rating = Column(Float, nullable=False)

    def __str__(self):
        return f'Anime title: {self.title}; Director: {self.director}; Rating: {self.rating}'


engine = create_engine('sqlite:///animes.db', echo=True, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


def password_validator(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True