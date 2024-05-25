from index import Index
from model import IRModel
from functools import reduce
import json, os
import matplotlib.pyplot as plt
from whoosh.scoring import BM25F
from doc2vec.doc2vec_model import Doc2VecModel
from sentiment.sentiment_model import SentimentWeightingModel, AdvancedSentimentWeightingModel, SentimentWeightingModelWeightedAverage, AdvancedSentimentWeightingModelWeightedAverage
def getResult(index, model, querytest, nResult):
    my_model = IRModel(index, model)
    _, result = my_model.search(query=querytest["query"], resLimit=nResult, sentiments=querytest["sentiments"])
    
    return [int(id) for id in result.keys()]


def getCampi(result, campi):
    strReturn = ""
    for numero in result:
        nome_file = f"{numero}.json"
        try:
            with open(f'./dataset/json/{nome_file}', 'r') as file:
                dati = json.load(file)
                risultato = {campo: dati.get(campo, 'Campo non trovato') for campo in campi}
                strReturn += f"File: {nome_file} \n"
                for campo, valore in risultato.items():
                    
                    if campo != "reviews":
                        strReturn += f"  {campo}: {valore}\n"
                    else:
                        strReturn += "REVIEWS:\n" +reduce(lambda x,y: x+"\n->"+y,[elem["review"] for elem in valore], "")
                        
                strReturn += "\n\n"  # Linea vuota per separare l'output dei file
        except FileNotFoundError:
            print(f"Errore: Il file {nome_file} non è stato trovato.")
        except json.JSONDecodeError:
            print(f"Errore: Il file {nome_file} non è un file JSON valido.")
    return strReturn

def testAllQueriesInADir():
    i = Index()
    # Models that need to be teste  d. 
    models = [
        (BM25F(), "BM25F"),
        (Doc2VecModel(), "Doc2Vec"),
        (SentimentWeightingModel(), "Base Sentiment"),
        (AdvancedSentimentWeightingModel(), "Advanced Sentiment" ),
        (SentimentWeightingModelWeightedAverage(), "Base Sentiment Weighted Average Based"),
        (AdvancedSentimentWeightingModelWeightedAverage(), "Advanced Sentiment Weighted Average Based")
    ]
    file_path = os.path.join("evaluation", "queries.json")
    
    with open(file_path) as f:
        queries = json.load(f)
    
    for c,q in enumerate(queries):
        
        for model, model_name in models:
            fileToSave = f'{q["UIN"]}\n'
            fileToSave += model_name + "\n"
            res = getResult(i, model,q, 20)
            fileToSave += "\t" + getCampi(res, ["id","name", "description","reviews"])
            fileToSave += "\n\n"
            with open(f'testDir/{c}_{model_name}.txt', 'w') as file:
                file.write(fileToSave)

if __name__ == "__main__":
    ### PER VEDERE LA DISTRIBUZIONE FAR AVVIARE QUESTO SCRIPT
    model = SentimentWeightingModel()
    file_path = os.path.join("evaluation", "queries.json")
    with open(file_path) as f:
        queries = json.load(f)
    i = Index()
    for c, q in enumerate(queries):
        print(f"Processing query {c}...")
        res = getResult(i,model,q,20)
        print(f"Completed!")
        model.getListLen()
    
    model.saveScoreListOnFile()
    ##### -------
    
    #### qua la recupera dal file e la plotta, quindi in caso commentare la parte sopra se hai già il file. 
    with open("scoreList.json", 'r') as file:
        lista = json.load(file)
    plt.hist(lista, bins=300, edgecolor='black', alpha=0.5, color='skyblue')
    plt.title('Distribuzione dei Numeri')
    plt.xlabel('Numero')
    plt.ylabel('Frequenza')
    plt.show()