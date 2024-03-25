import pickle
from Sentiment.extractEmotions import ExtractEmotions
import yaml
import os
import json

class ReviewsIndex:
	def __init__(self, path = "./dataset/reviews.pickle"):
		if(not os.path.exists(path)):
			self.setupReviewDB()
		with open(path, "rb") as fp:
			self.index = pickle.load(fp)	

	def get_sentiments(self, id):
		return self.index.get(id)
 
	def setupReviewDB(self):
		print("Building reviews pickle file... ")
		SENTIMENTS= ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"] 

		sentiment = ExtractEmotions()

		with open('config.yaml','r') as file:
			config_data = yaml.safe_load(file)

		dataDir = f"./{config_data['REVIEWS']['DATADIR']}" 
		revF = open(f"./{config_data['REVIEWS']['FILE']}", mode='wb')
		reviewsDict = {}
			
		for i,jsonFile in enumerate(os.listdir(dataDir)):
			with open(u"{dir}/{file}".format(dir=dataDir, file=jsonFile), "r", encoding="utf-8") as f:				
				
				data = json.load(f)
				reviewsDict[data["id"]]={}
				nrReview=len(data["reviews"])
				for s in SENTIMENTS:
					reviewsDict[data["id"]][s]=0
		
				for review in data["reviews"]:
					try:
						sentiments = sentiment.extract(review["review"])
					except Exception as e:
						print(e)
					for sent in sentiments:
						for s in sent:
							reviewsDict[data["id"]][s["label"]]+=(s["score"]/nrReview)

			if i>1000:
				break
		pickle.dump(reviewsDict, revF)
		print("Review pickle file created successfully! ")		

if __name__ == "__main__":
    #setupReviewDB()
    rew = ReviewsIndex()
    print(rew.index.get(10006571))