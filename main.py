from index import Index
from gui.main_gui import MyGUI
from controller import Controller
from model import IRModel
from sentiment.sentiment_model import SentimentModelARWA, SentimentModelWA
from doc2vec.doc2vec_model import Doc2VecModel
from model import IRModel
from whoosh.scoring import BM25F
import argparse


def setupParser() -> list: 
    parser = argparse.ArgumentParser(description='Choose the model.')
    
    parser.add_argument('--build-index', action='store_true', 
                help='Force a new build of the index.')
    
    group = parser.add_mutually_exclusive_group()
    
    group.add_argument('-B', required=False, action='store_true',
            help='Default model which is the BM25F')
    
    group.add_argument('-S', required=False, action='store_true',
                help='Sentiment Weighting Model based on 7 sentiments.')
    
    group.add_argument('-RS', required=False, action='store_true',
                help='Sentiment Weighting model based on 7 sentiments and on amount of Reviews.')
    
    group.add_argument('-D2V', required=False, action='store_true',
                help='Document To Vector model.')
    
    args = parser.parse_args()

    if not any([args.B, args.S, args.RS, args.D2V]):
        args.B = True
            
    active_arg = None
    if args.B:
        active_arg = 'B'
    elif args.S:
        active_arg = 'S'
    elif args.RS:
        active_arg = 'RS'
    elif args.D2V:
        active_arg = 'D2V'

    return (args.build_index, active_arg)


def main(buildInd, model: str) -> None:
    my_index = Index(forceBuildIndex=buildInd)
    
    modelsDict = {
        'B' : (BM25F(), "Base Model"),
        'D2V' : (Doc2VecModel(), "Doc 2 Vec"),
        'S' : (SentimentModelWA(), "Sentiment Weighting Model"),
        'RS' : (SentimentModelARWA(),"Sentiment Weighting Model - Amount Reviews Based"),  
    }

    customModel = IRModel(my_index, modelsDict[model][0])
        
    control = Controller(my_index, customModel)
    MyGUI(control, modelsDict[model][1])


if __name__ == "__main__":
    forceBuildIndex, model = setupParser()
    main(forceBuildIndex, model)

