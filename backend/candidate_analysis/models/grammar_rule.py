#import sys
#sys.path.append('/home/abhishek/candidate-analysis/candidate_analysis/backend/')
from candidate_analysis.framework.db import db
from candidate_analysis.framework.utils import from_root_path
import pandas as pd
from pandas.io import sql
# import psycopg2
# from sqlalchemy import create_engine



class GrammarRule(db.Model):
    __tablename__ = 'grammar_rules'
    grammar_rule_id = db.Column(db.String(100), primary_key=True)
    grammar_rules_category = db.Column(db.String(80))
    score = db.Column(db.Float)

    def __repr__(self):
        return '<GrammarRule %r>' % self.grammar_rule_id

    @classmethod
    def import_csv_to_sql(cls):
        dataframe = pd.read_csv(from_root_path('data/grammar_rules.csv'))
        
        dataframe = dataframe.drop(['Example'],1)
        dataframe.columns = ['grammar_rule_id','grammar_rules_category','score']
        dataframe = dataframe[dataframe.grammar_rule_id.notnull()]
        
        exsisting_ids = []
        result = GrammarRule.query.all()
        for r in result:
          exsisting_ids.append(r.grammar_rule_id)
        
        for i in dataframe.index:
          row = dataframe.loc[i]
          if row.grammar_rule_id in exsisting_ids:
            dataframe = dataframe.drop([i])

        print("Data to be inserted are: ")
        print(dataframe)
        
        # engine = create_engine('postgresql://postgres:mindfire@localhost:5432/candidate_analysis')
        # with engine.connect() as conn, conn.begin():
        dataframe.to_sql('grammar_rules', db.engine, if_exists='append',index = False)





