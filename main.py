from index import Index
from gui.main_gui import MyGUI
from controller import Controller
from model import IRModel
from sentiment.sentiment_model import AdvancedSentimentWeightingModel, SentimentWeightingModel
from doc2vec.doc2vec_model import Doc2VecModel
from model import IRModel
from whoosh.scoring import BM25F
import argparse


def setupParser() -> list: 
    parser = argparse.ArgumentParser(description='Choose the model.')
    
    group = parser.add_mutually_exclusive_group()
    
    group.add_argument('-S', required=False, action='store_true',
                    help='Sentiment Weighting Model based on 7 sentiments.')
    
    group.add_argument('-AS', required=False, action='store_true',
                    help='Advancend Sentiment Weighting model based on 7 sentiments and on recentness of reviews.')
    
    group.add_argument('-D2V', required=False, action='store_true',
                help='Document To Vector model.')
    
    model = [k for k, v in vars(parser.parse_args()).items() if v]

    if len(model) == 0: 
        return 'B'
    else: 
        return model[0]


def main(model: str) -> None:
    my_index = Index()
    
    modelsDict = {
        'B' : (BM25F(), "Base Model"),
        'D2V' : (Doc2VecModel(), "Doc 2 Vec"),
        'S' : (SentimentWeightingModel(), "Sentiment Weighting Model"),
        'AS' : (AdvancedSentimentWeightingModel(),"Advanced Sentiment Weighting Model") 
    }

    customModel = IRModel(my_index, modelsDict[model][0])
        
    control = Controller(my_index, customModel)
    MyGUI(control, modelsDict[model][1])
    

if __name__ == "__main__":
    model = setupParser()
    main(model)

