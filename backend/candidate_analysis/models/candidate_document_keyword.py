from candidate_analysis.framework.db import db
from candidate_analysis.models.keyword import Keyword

class CandidateDocumentKeyword(db.Model):
    __tablename__ = 'candidate_document_keywords'
    candidate_document_id = db.Column(db.Integer, db.ForeignKey('candidate_documents.candidate_document_id'), primary_key=True)
    keyword_id = db.Column(db.Integer, db.ForeignKey('keywords.keyword_id'), primary_key=True)
    density = db.Column(db.Float)

    def __repr__(self):
        return '<CandidateDocumentKeyword %r>' % self.candidate_document_id


    @classmethod
    def get_document_keywords_density(cls, doc_id):
        result = CandidateDocumentKeyword.query.filter_by(candidate_document_id = doc_id)
        doc_keyword_density = {}
        for res in result:
            key_id = res.keyword_id
            #print("Keyword_id : ", key_id)
            key_name = Keyword.query.filter_by(keyword_id = key_id).first().keyword
            #key_name = key_object.keyword
            key_density = res.density

            doc_keyword_density[key_name] = key_density

        return doc_keyword_density




