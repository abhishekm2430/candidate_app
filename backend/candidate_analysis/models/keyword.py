from candidate_analysis.framework.db import db
from sqlalchemy.dialects.postgresql import JSON
from candidate_analysis.framework.utils import from_root_path
import pandas as pd
from pandas.io import sql

class Keyword(db.Model):
    __tablename__ = 'keywords'
    keyword_id = db.Column(db.Integer, primary_key=True)
    keyword_type = db.Column(db.String(80))
    keyword_tags_json = db.Column(JSON)
    raw_text = db.Column(db.Text)
    keyword = db.Column(db.String(80))
    validated = db.Column(db.Boolean)

    def __repr__(self):
        return '<Keyword %r>' % self.keyword_id

    @classmethod
    def import_keywords_to_sql(cls):
        #dataframe = pd.read_csv('/home/abhishek/technologies.csv')
        dataframe = pd.read_csv(from_root_path('data/technologies.csv'))
        dataframe = dataframe.drop(['Category'],1)
        dataframe.columns = ['keyword_type', 'raw_text', 'keyword', 'validated']
        print(dataframe.head())
        dataframe = dataframe.drop(['validated'], 1)
        exsisting_ids = []
        result = Keyword.query.all()
        for r in result:
            exsisting_ids.append(r.keyword)

        for i in dataframe.index:
            row = dataframe.loc[i]
            if row.keyword in exsisting_ids:
                dataframe = dataframe.drop([i])
        # dataframe.validated[dataframe.validated == 0] = False
        # dataframe.validated[dataframe.validated == 1] = True
        print(dataframe)
        dataframe.to_sql('keywords', db.engine, if_exists='append',index = False)

