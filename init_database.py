import json
import re
from models import db, ArxivPaper, Author
from flask import Flask
from sqlalchemy import create_engine
from datetime import datetime
from tqdm import tqdm
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from collections import defaultdict

ARXIV_ID_PATTERN = r'\d{4}\.\d{4,5}'

def get_arxiv_papers_json():
    with open('arxiv-metadata-oai-snapshot.json') as f:
        arxiv_papers_json = []
        print('Reading arxiv papers in json from disk.')
        for line in tqdm(f.readlines()):
            arxiv_papers_json.append(json.loads(line))
    arxiv_papers_json = [x for x in arxiv_papers_json if re.match(ARXIV_ID_PATTERN, x['id'])]
    return arxiv_papers_json

# Create a Flask app and configure the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arxiv_papers.db'
db.init_app(app)

# Create the database tables
def recreate_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
    
def get_papers():
    new_papers = []
    arxiv_papers_json = get_arxiv_papers_json()
    print('Converting arxiv papers to classes.')
    for paper in tqdm(arxiv_papers_json):
        new_papers.append({
            'id': paper['id'],
            'submitter': paper['submitter'],
            'title': paper['title'],
            'comments': paper.get('comments', ''),
            'journal_ref': paper.get('journal-ref', ''),
            'doi': paper.get('doi', ''),
            'report_no': paper.get('report-no', ''),
            'categories': paper['categories'],
            'license': paper.get('license', ''),
            'abstract': paper['abstract'],
            'update_date': datetime.strptime(paper['update_date'], '%Y-%m-%d').date(),
            'created_date': datetime.strptime(paper['versions'][0]['created'], '%a, %d %b %Y %H:%M:%S %Z')
        })
    return new_papers

    
def commit_arxiv_papers():
    new_papers = get_papers()
    with app.app_context():
        Session = sessionmaker(bind=db.engine)
        session = Session()

        try:
            # Get existing paper IDs
            existing_paper_ids = set(session.query(ArxivPaper.id).all())

            # Bulk insert new papers
            session.bulk_insert_mappings(ArxivPaper, new_papers)
            session.flush()
            session.commit()
            print(f'{len(new_papers)} ArxivPapers committed.')
        except IntegrityError as e:
            session.rollback()
            print(f"An error occurred: {e}")
        finally:
            session.close()
recreate_database()    
commit_arxiv_papers()
