from candidate_analysis.framework.db import db

class CandidateDocumentLine(db.Model):
    __tablename__ = 'candidate_document_lines'
    candidate_document_lines_id = db.Column(db.Integer, primary_key=True)
    candidate_document_id = db.Column(db.Integer, db.ForeignKey('candidate_documents.candidate_document_id'), nullable=False)
    document_line_text = db.Column(db.Text)
    grammar_issue = db.Column(db.Boolean)
    grammar_score = db.Column(db.Float)

    def __repr__(self):
        return '<CandidateDocumentLine %r>' % self.candidate_document_lines_id
