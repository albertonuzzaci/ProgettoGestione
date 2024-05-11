
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import json, yaml, os, math

# define a list of documents.

docs=[]
with open('../config.yaml','r') as file:
	config_data = yaml.safe_load(file)
dataDir = f"../{config_data['REVIEWS']['DATADIR']}" 
 
for i,jsonFile in enumerate(os.listdir(dataDir)):
    with open(u"{dir}/{file}".format(dir=dataDir, file=jsonFile), "r", encoding="utf-8") as f:
        data = json.load(f)

        if type(data["description"])==float:
            docs.append(data["name"])
        else:
            docs.append(data["name"]+" "+data["description"])

# preproces the documents, and create TaggedDocuments
tagged_docs = [TaggedDocument(words=word_tokenize(doc.lower()),tags=[str(i)]) for i, doc in enumerate(docs)]

# train the Doc2vec model
model = Doc2Vec(vector_size=20,
                min_count=2, epochs=50)
model.build_vocab(tagged_docs)
model.train(tagged_docs,
            total_examples=model.corpus_count,
            epochs=model.epochs)
 
# get the document vectors
document_vectors = [model.infer_vector(
    word_tokenize(doc.lower())) for doc in docs]

model.save("doc2vec_model")
#  print the document vectors
""" for i, doc in enumerate(docs):
    print("Document", i+1, ":", doc)
    print("Vector:", document_vectors[i])
    print() """