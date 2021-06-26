from candidate_analysis.framework.db import db
from sqlalchemy.dialects.postgresql import JSON
from candidate_analysis.models import CandidateDocumentKeyword

class CandidateDocument(db.Model):
    __tablename__ = 'candidate_documents'
    candidate_document_id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.candidate_id'), nullable=False)
    document_path = db.Column(db.Text)
    document_metadata_json = db.Column(JSON)
    grammar_score = db.Column(db.Float)
    document_json = db.Column(JSON)
    technology_json = db.Column(JSON)
    technology_category_json = db.Column(JSON)

    keywords = db.relationship('Keyword', secondary='candidate_document_keywords', lazy='subquery', backref=db.backref('candidate_documents', lazy=True))
    candidate_document_lines = db.relationship('CandidateDocumentLine', backref='CandidateDocument', lazy=True)

    def __repr__(self):
        return '<CandidateDocument %r>' % self.candidate_document_id
