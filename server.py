from flask import Flask, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db, ArxivPaper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arxiv_papers.db'
db.init_app(app)

@app.route('/')
def home():
    with app.app_context():
        return render_template('index.html', history=ArxivPaper.query.limit(5).all())
    
@app.route('/paper/<string:paper_id>')
def paper(paper_id):
    with app.app_context():
        return render_template('paper.html', paper=ArxivPaper.query.filter_by(id=paper_id).first())

if __name__ == '__main__':
    app.run(debug=True)