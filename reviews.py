
import os
import json
import yaml
from sentiment import ExtractEmotions
import pickle

class ReviewsDict:
	SENTIMENTS= ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"] 
	def __init__(self):
		self.reviews = self.setupReviewDB()
  
	def setupReviewDB(self):
     
		sentiment = ExtractEmotions()
  
		with open('config.yaml','r') as file:
			config_data = yaml.safe_load(file)
   
		dataDir = f"./{config_data['REVIEWS']['DATADIR']}" 
		revF = open(f"./{config_data['REVIEWS']['FILE']}", mode='wb')
		reviewsDict = {}
           
		for jsonFile in os.listdir(dataDir):
			with open(u"{dir}/{file}".format(dir=dataDir, file=jsonFile), "r", encoding="utf-8") as f:				
				
				data = json.load(f)
				reviewsDict[data["id"]]={}
				nrReview=len(data["reviews"])
				for s in ReviewsDict.SENTIMENTS:
					reviewsDict[data["id"]][s]=0
     
				for review in data["reviews"]:
					try:
						sentiments = sentiment.extract(review["review"])
					except Exception as e:
						print(e)
					for sent in sentiments:
						for s in sent:
							reviewsDict[data["id"]][s["label"]]+=(s["score"])/nrReview
      
		pickle.dump(reviewsDict, revF)
  
class ReviewsIndex:
	def __init__(self, path = "./dataset/reviews.pickle"):
		with open(path, "rb") as fp:
			self.index = pickle.load(fp)			

if __name__ == "__main__":
    #r = ReviewsDict()
    rew = ReviewsIndex()
    print(rew.index[20069801])