import yaml, os
import json

from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh import index

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


class Index():
    
    def __init__(self, forceBuildIndex=False, limit=None):
        self.schemaAcc = self.setupSchemaAcc()
        self.indexAcc = self.setupIndexAcc(forceBuildIndex, limit)
            
    def setupSchemaAcc(self):
        schema = Schema(
            id = ID(stored=True, unique=True),
            #listing_url = TEXT(stored=True),
            name = TEXT(stored=True, field_boost=2.0, spelling=True),
            description = TEXT(stored=True),
            #host_name = TEXT(stored=True),
            #host_id = ID(),
            #host_url = TEXT(stored=True),
            #host_picture_url = TEXT(stored=True),
            neighbourhood_cleansed = TEXT(stored=True),
            #latitude = NUMERIC(stored=True, numtype=float),
            #longitude = NUMERIC(stored=True, numtype=float),
            #property_type = TEXT(stored=True),
            #room_type = TEXT(stored=True),
            accomodates = NUMERIC(stored=True, numtype=float),
            bathrooms = NUMERIC(stored=True, numtype=float),
            #bedrooms = NUMERIC(stored=True),
            beds = NUMERIC(stored=True),
            #amenities = KEYWORD(stored=True, commas=True),
            price = NUMERIC(stored=True, numtype=float),
            #numbers_of_review = NUMERIC(stored=True,numtype=float),
            review_scores_rating = NUMERIC(stored=True, numtype=float)
        )
        return schema
    
    def setupIndexAcc(self, forceBuildIndex, limit):
        with open('config.yaml','r') as file:
            config_data = yaml.safe_load(file)
        
        if not os.path.exists(f"{config_data['INDEX']['MAINDIR']}/{config_data['INDEX']['ACCDIR']}") or forceBuildIndex:
            return self.createIndexAcc(limit)
        else:
            return index.open_dir(f"{config_data['INDEX']['MAINDIR']}/{config_data['INDEX']['ACCDIR']}")
    
    def createIndexAcc(self, limit):

        with open('config.yaml','r') as file:
            config_data = yaml.safe_load(file)
        try:
            if not os.path.exists(f"{config_data['INDEX']['MAINDIR']}"):
                os.mkdir(f"{config_data['INDEX']['MAINDIR']}")
            
            os.mkdir(f"{config_data['INDEX']['MAINDIR']}/{config_data['INDEX']['ACCDIR']}")
        except FileExistsError:
            pass        
            
        data_dir = f"./{config_data['DATASET']['DATADIR']}"
        ix = index.create_in(f"{config_data['INDEX']['MAINDIR']}/{config_data['INDEX']['ACCDIR']}", self.schemaAcc)
        writer = ix.writer()
        
        
        for i, jsonFile in enumerate(os.listdir(data_dir)):
            with open(u"{dir}/{file}".format(dir=data_dir, file=jsonFile), "r", encoding="utf-8") as f:
                data = json.load(f)
                print(u"{dir}/{file}".format(dir=data_dir, file=jsonFile))
                writer.add_document(
                    id = str(data["id"]),
                    #listing_url = str(data["listing_url"]),
                    name = str(data["name"]),
                    description = str(data["description"]),
                    #host_name = str(data["host_name"]),
                    #host_id = str(data["host_id"]),
                    #host_url = str(data["host_url"]),
                    #host_picture_url = str(data["host_picture_url"]),
                    neighbourhood_cleansed = str(data["neighbourhood_cleansed"]),
                    #latitude = data["latitude"],
                    #longitude = data["longitude"],
                    #property_type = str(data["property_type"]),
                    #room_type = str(data["room_type"]),
                    accomodates = data["accommodates"],
                    bathrooms = data["bathrooms"],
                    #bedrooms = data["bedrooms"],
                    beds = data["beds"],
                    #amenities = ",".join(data["amenities"]) if data["amenities"] != None else None,
                    price = data["price"],
                    #numbers_of_review = data["numbers_of_review"],
                    review_scores_rating = data["review_scores_rating"]
                )
                if limit != None and i > limit:
                    break
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
  

if __name__ == '__main__':
    my_index = Index(forceBuildIndex=False, limit=1000)
    #r = searchAcc(my_index, "bed AND (neighbourhood_cleansed:(\"Westminster\" OR \"Waltham Forest\"))", 10)

