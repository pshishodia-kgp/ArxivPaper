from flask import Flask, jsonify, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from models import db, ArxivPaper, User, List


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arxiv_papers.db'
app.config['SECRET_KEY'] = 'your-secret-key'  # Add a secret key for Flask-Login
db.init_app(app)

ADMIN_USER = None
with app.app_context():
    ADMIN_USER = User.query.filter_by(username='pshishodia').first()
user = ADMIN_USER

@app.route('/')
def home():
    return render_template('index.html', history=ArxivPaper.query.limit(5).all())

@app.route('/lists')
def lists():
    return render_template('lists.html', lists=List.query.filter_by(owner_username=user.username).all())

@app.route('/create_list', methods=['POST'])
def create_list():
    list_name = request.form.get('list_name')
    new_list = List(name=list_name, owner_username=user.username)
    db.session.add(new_list)
    db.session.commit()
    return redirect('/lists')

@app.route('/list/<int:list_id>')
def list(list_id):
    return render_template('list_view.html', list = List.query.filter_by(id=list_id).first())
    
@app.route('/paper/<string:paper_id>')
def paper(paper_id):
    return render_template('paper.html', paper=ArxivPaper.query.filter_by(id=paper_id).first())

if __name__ == '__main__':
    app.run(debug=True)