from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ArxivPaper(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    submitter = db.Column(db.String(100))
    title = db.Column(db.Text)
    comments = db.Column(db.Text)
    journal_ref = db.Column(db.String(200))
    doi = db.Column(db.String(100))
    report_no = db.Column(db.String(100))
    categories = db.Column(db.String(100))
    license = db.Column(db.String(100))
    abstract = db.Column(db.Text)
    update_date = db.Column(db.Date)
    
    created_date = db.Column(db.DateTime) # date for the first version.

    authors = db.relationship('Author', secondary='paper_authors', back_populates='papers')
    lists = db.relationship('List', secondary='list_papers', back_populates='papers')

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    middle_name = db.Column(db.String(100))
    papers = db.relationship('ArxivPaper', secondary='paper_authors', back_populates='authors')

paper_authors = db.Table('paper_authors',
    db.Column('paper_id', db.String(20), db.ForeignKey('arxiv_paper.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True)
)

class User(db.Model):
    username = db.Column(db.String(100), primary_key=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    lists = db.relationship('List', back_populates='owner')

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner_username = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    owner = db.relationship('User', back_populates='lists')
    papers = db.relationship('ArxivPaper', secondary='list_papers', back_populates='lists')

list_papers = db.Table('list_papers',
    db.Column('list_id', db.Integer, db.ForeignKey('list.id'), primary_key=True),
    db.Column('paper_id', db.String(20), db.ForeignKey('arxiv_paper.id'), primary_key=True)
)