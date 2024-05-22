import pickle
from sentiment.extract_emotions import ExtractEmotions
import yaml
import os
import json


class ReviewsIndex:
	def __init__(self):
		with open('./config.yaml','r') as file:
			config_data = yaml.safe_load(file)
		
		path = f"./{config_data['REVIEWS']['FILE']}" 
		if(not os.path.exists(path)):
			self.setupReviewDB()
		with open(path, "rb") as fp:
			self.index = pickle.load(fp)	

	def get_sentiments(self, id):
		return self.index.get(id)[0]

	""" 
	Stores in a pickle file a dict containing, for each apartment (id), the reviews sentiments vectors and the amount of reviews, 
 	i.e. a dict with that structure:
		id: ({"anger":x_1, "disgust":x_2, "fear":x_3, "joy":x_4, "neutral":x_5, "sadness":x_6, "surprise":x_7}, int),
		..., 
  
	Actually each sentiment score (x_n) is an overall (mean) value of that sentiment based on all reviews of that apartment.
 	"""

	def setupReviewDB(self):
		print("Building reviews pickle file... ")
		SENTIMENTS= ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"] 

		sentiment = ExtractEmotions()

		with open('./config.yaml','r') as file:
			config_data = yaml.safe_load(file)

		dataDir = f"./{config_data['REVIEWS']['DATADIR']}" 
		
		reviewsDict = {}
			
		for i,jsonFile in enumerate(os.listdir(dataDir)):
			with open(u"{dir}/{file}".format(dir=dataDir, file=jsonFile), "r", encoding="utf-8") as f:				
				
				data = json.load(f)
				nrReview=len(data["reviews"])

				reviewsDict[data["id"]] = (dict(),nrReview)
    
				for s in SENTIMENTS:
					reviewsDict[data["id"]][0][s]=0
		
				for review in data["reviews"]:
					try:
						#if not math.isnan(review["review"]):
						sentiments = sentiment.extract(review["review"])
					except Exception as e:
						print(data["id"])
						print(e)
      
					for sent in sentiments:
						for s in sent:
							reviewsDict[data["id"]][0][s["label"]]+=(s["score"]/nrReview)

		with open(f"./{config_data['REVIEWS']['FILE']}", mode='wb') as revF:
			pickle.dump(reviewsDict, revF)
		
		print("Review pickle file created successfully! ")

	def get_sentiment_len_for(self, key):
		return self.index.get(int(key))[1]

if __name__ == "__main__":
    #setupReviewDB()
    rev = ReviewsIndex()
    print(rev.index.get(10094145))
