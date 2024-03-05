import yaml, os, shutil
import pandas as pd
from functools import reduce

from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, DATETIME, NUMERIC
from whoosh import index, scoring
from whoosh.index import open_dir
from whoosh import qparser
from whoosh import query

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

class Index():
    
    def __init__(self, forceBuildIndex=False):
        self.schemaAcc = self.setupSchemaAcc()
        self.indexAcc = self.setupIndexAcc(forceBuildIndex)
        
        self.schemaRev = self.setupSchemaRev()
        self.indexRev = self.setupIndexRev(forceBuildIndex)
            
    def setupSchema(self):
        schema = Schema(
            recipe_name=TEXT(stored=True),
            recipe_ID=ID(),
            minutes = NUMERIC(stored=True),
            contributor_ID = ID(),
            date = DATETIME(),
            tags = KEYWORD(stored=True, commas=True),
            nutrions = NUMERIC(stored=True),
            steps = TEXT(),
            description = TEXT(stored=True),
            description_preprocessed = KEYWORD(),
            ingredients =  KEYWORD(stored=True, commas=True),
            n_ing = NUMERIC() 
        )
        return schema
    
    def setupIndex(self, forceBuildIndex):
        with open('config.yaml','r') as file:
            config_data = yaml.safe_load(file)
        
        if not os.path.exists(f"{config_data['INDEX']['MAINDIR']}/{config_data['INDEX']['RECIPESDIR']}") or forceBuildIndex:
            return self.createIndex()
        else:
            return index.open_dir(f"{config_data['INDEX']['MAINDIR']}/{config_data['INDEX']['RECIPESDIR']}")
    
    def createIndex(self):

        with open('config.yaml','r') as file:
            config_data = yaml.safe_load(file)
        try:
            if not os.path.exists(f"{config_data['INDEX']['MAINDIR']}"):
                os.mkdir(f"{config_data['INDEX']['MAINDIR']}")
            
            os.mkdir(f"{config_data['INDEX']['MAINDIR']}/{config_data['INDEX']['RECIPESDIR']}")
        except FileExistsError:
            pass        
            
        data_dir = f"./{config_data['DATASET']['DATADIR']}/{config_data['INDEX']['FILERECIPE']}"
        ix = index.create_in(f"{config_data['INDEX']['MAINDIR']}/{config_data['INDEX']['RECIPESDIR']}", self.schema)
        writer = ix.writer()
        
        df = pd.read_csv(data_dir)
        
        for i, row in df.iterrows():
            writer.add_document(
                recipe_name=str((row['name'])),
                recipe_ID=str(row['id']),
                minutes = int(row['minutes']),
                contributor_ID = str(row['contributor_id']),
                date = str(row['submitted']),
                tags = str(", ".join(eval(row['tags']))),
                nutrions = float(eval(row['nutrition'])[0]),
                steps = str(", ".join(eval(row['steps']))),
                description = str(row['description']),
                description_preprocessed = str(IndexRecipies.preprocessing(row['description'])),
                ingredients =  str(", ".join(eval(row['ingredients']))),
                n_ing = int(row['n_ingredients']) 
            )
            if i > 1000:
                writer.commit()
                return ix
            
    @staticmethod
    def preprocessing(text):
        tokens = nltk.word_tokenize(str(text))
        porter = PorterStemmer()
        tagged = nltk.pos_tag(tokens)
        stop_words = set(stopwords.words('english'))
        text_processed = set()
        for t in tokens:
            if t not in stop_words:
                tt = nltk.pos_tag([t])
                if tt[0][1][0:2] == 'NN':
                    text_processed.add(porter.stem(t))
        text_stemmed = " ".join(text_processed) 
        return text_stemmed

def search(my_index: IndexRecipies):
    try:
        s = my_index.ix.searcher()
        #qp = qparser.QueryParser("recipe_name", schema=my_index.schema)
    
        qp = qparser.MultifieldParser(['recipe_name','description'], schema=my_index.schema, group=qparser.OrGroup)
        while (True):
            print("Insert query-> ")
            q = input()
            
            parsedQ = qp.parse(q)
            print(f"Parsed query: {parsedQ}")
            results = s.search(parsedQ, terms=True, limit=50)
            if results.estimated_length() == 0:
                print("Nothing found!")
            else:
                print(f"Results scored lenght: {results.scored_length()}")
                #print(reduce(lambda x,y: x+str(y)+'\n\n', results, ""))
                
                
                for c, hit in enumerate(results):
                    print(f"----------------HIT{c}-------------")
                    print(hit.matched_terms())
                    print(f'Recipe name: {hit["recipe_name"]}')
                    print(f'Description: {hit["description"]}')
                    print(f'Ingredients: {hit["ingredients"]}')
                    print(f'Tags: {hit["tags"]}')
                    print("\n")
                    #print(f"Contains: {hit.matched_terms()}")
                    #print("Doesn't contain:", query.all_terms().difference(set(hit.matched_terms())))
                
            '''
            found = results.scored_length()
            if results.has_exact_length():
                print("Scored", found, "of exactly", len(results), "documents")
            else:
                low = results.estimated_min_length()
                high = results.estimated_length()

                print("Scored", found, "of between", low, "and", high, "documents")
            '''
    except Exception as e: 
        print(e)
    finally:
        s.close()

if __name__ == '__main__':
    my_index = IndexRecipies()
    search(my_index)
    '''
    s = my_index.ix.searcher()
    results = s.search(query.Every(), terms=True)
    print(results[0]["description"])
    print(results[0]["ingredients"])
    print(results[0]["tags"])
    print(results[0]["minutes"])
    print(results[0]["nutrions"])
    '''