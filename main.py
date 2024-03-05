import pandas as pd
import os
import opendatasets as od
from setup import myDataset

import yaml
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, DATETIME, NUMERIC
from whoosh.analysis import StemmingAnalyzer
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
import os, os.path
from whoosh import index
from whoosh.query import Every

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

def createSchema():
    schema = Schema(
        recipe_name=TEXT(stored=True),
        recipe_ID=ID(stored=True),
        minutes = NUMERIC(stored=True),
        contributor_ID = ID(stored=True),
        date = DATETIME(stored=True),
        tags = KEYWORD(stored=True),
        nutrions = NUMERIC(stored=True),
        steps = TEXT(stored=True),
        description = TEXT(stored=True),
        #description_preprocessed = KEYWORD,
        ingredients =  KEYWORD(stored=True, commas=True),
        n_ing = NUMERIC(stored=True) 
    )
    return schema





def create_index():
    data_dir = './dataset/RAW_recipes.csv'
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

    schema = createSchema()
    ix = index.create_in("indexdir", schema)
    writer = ix.writer()

    df = pd.read_csv(data_dir)

    for i, row in df.iterrows():
        writer.add_document(
            recipe_name=str((row['name'])),
            recipe_ID=str(row['id']),
            minutes = int(row['minutes']),
            contributor_ID = str(row['contributor_id']),
            date = str(row['submitted']),
            tags = str(row['tags']),
            nutrions = float(eval(row['nutrition'])[0]),
            steps = str(", ".join(eval(row['steps']))),
            description = str(row['description']),
            #description_preprocessed = str(preprocessing(row['description'])),
            ingredients =  str(", ".join(eval(row['ingredients']))),
            n_ing = int(row['n_ingredients']) 
        )
        if(i>50):
            writer.commit()
            return
        

def preprocessing(text):
    tokens = nltk.word_tokenize(text)
    porter = PorterStemmer()

    stop_words = set(stopwords.words('english'))
    text_processed = set()
    for t in tokens:
        if t not in stop_words:
            tt = nltk.pos_tag([t])
            if tt[0][1][0:2] == 'NN':
                text_processed.add(porter.stem(t))
    text_stemmed = " ".join(text_processed)
    return text_stemmed




def search():
    ix = open_dir("indexdir")
    try:
        s = ix.searcher()
        parser = QueryParser("recipe_name", schema=ix.schema)
        while (True):
            print("Insert query-> ")
            q = input()
            query = parser.parse(u""+q)
            results = s.search(query)
            if len(results)==0:
                print("Nothing found!")
            else:
                print(results.fields())
    except: 
        print("ERRORE")
    finally:
        s.close()
    
    




if __name__ == "__main__":
    
    
