import pickle

class ReviewsIndex:
	def __init__(self, path = "./dataset/reviews.pickle"):
		with open(path, "rb") as fp:
			self.index = pickle.load(fp)	

	def get_sentiments(self, id):
		return self.index.get(id)
 

		

if __name__ == "__main__":
    #setupReviewDB()
    rew = ReviewsIndex()
    print(rew.index.get(10006571))