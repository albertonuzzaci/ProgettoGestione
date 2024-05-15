
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from whoosh.analysis import StandardAnalyzer
import json, yaml, os

# define a list of documents.

def doc2vec_creation():
    docs=[]
    with open('../config.yaml','r') as file:
        config_data = yaml.safe_load(file)
    
    dataDir = f"../{config_data['REVIEWS']['DATADIR']}" 
    
    for jsonFile in os.listdir(dataDir):
        with open(u"{dir}/{file}".format(dir=dataDir, file=jsonFile), "r", encoding="utf-8") as f:
            data = json.load(f)
            
            if isinstance(data["description"],float):
                docs.append(data["name"])
            else:
                docs.append(f'{data["name"]} {data["description"]}')

    # preproces the documents, and create TaggedDocuments
    analyzer = StandardAnalyzer()
    tagged_docs = [TaggedDocument(words=[token.text for token in analyzer(doc)],tags=[str(i)]) for i, doc in enumerate(docs)]

    # train the Doc2vec model
    model = Doc2Vec(vector_size=20,
                    min_count=1, epochs=50, workers=8)
    
    model.build_vocab(tagged_docs)
    
    model.train(tagged_docs,
                total_examples=model.corpus_count,
                epochs=model.epochs)
    
    """ # get the document vectors
    document_vectors = [model.infer_vector(
        word_tokenize(doc.lower())) for doc in docs] """

    model.save("doc2vec.model")

def to_json():
    model = Doc2Vec.load("doc2vec.model")  # load the model
    docs_vector = {}
    
    with open('../config.yaml','r') as file:
        config_data = yaml.safe_load(file)
    
    dataDir = f"../{config_data['REVIEWS']['DATADIR']}" 
    
    for i,jsonFile in enumerate(os.listdir(dataDir)):
        with open(u"{dir}/{file}".format(dir=dataDir, file=jsonFile), "r", encoding="utf-8") as f:
            data = json.load(f)
            docs_vector[data["id"]]=model.dv[i]
    
    serializable_docs_vector = {key: value.tolist() for key, value in docs_vector.items()}
    json_path = 'docs_vectors.json'  # json file path
    with open(json_path, 'w') as json_file:
        json.dump(serializable_docs_vector, json_file)  

    
    
if __name__ == "__main__":
    try:
        if not os.path.exists("doc2vec.model"):
            doc2vec_creation()
    except FileExistsError:
        pass 
    try:
        if not os.path.exists("docs_vectors.json"):
            to_json()
    except FileExistsError:
        pass
