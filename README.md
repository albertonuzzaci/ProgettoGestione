# London Accommodations Search-Engine

## Installation

Download the repository:  
```
git clone https://github.com/albertonuzzaci/ProgettoGestione.git
```  
In the main directory uncompress the dataset in order to have: 
```
mainDir/dataset/json/
mainDir/dataset/information.json
mainDir/dataset/reviews.pickle
```

It is advised to download used libraries in a virtual environment.
```
python -m venv venv
source activate
```
It may change depending on the operating system.

Install dependecies (be aware to be in the virtual environment directory):  
```
pip install -r requirements.txt
```  

## Usage
Run the search engine
```
python main.py [-h] [--build-index] [-B | -S | -AS | -D2V]
```  

Options: 
* ```-h, --help``` show an help message and exit. 
* ```--build-index``` build again the index. 
* ```[-B | -S | -AS | -D2V]``` choose the weighting model to run. 
	* ```-B``` run the search engine using the ```BM25F``` weighting model. This model is the default used in ```whoosh```. Without any option it will be taken as the **default** model. 
	* ```-S``` run the search engine using the ```SentimentWeightingModel``` weighting model. During the search a user can sort the results based on the feelings searched for. 
	* ```-AS```run the search engine using the ```AdvancedSentimentWeightingModel``` weighting model. During the search a user can sort the results based on the feelings searched for and at the same time on the quantity of reviews.
	* ```-D2V``` run the search engine using the ```Doc2VecModel``` weighting model. It use *doc2vec* which is a technique for generating vector representations of documents, allowing for efficient comparison and analysis of their semantic meanings.

Running requires
* **Index**: highly optimized data structure that contains indexed documents and their associated information, enabling fast and efficient text search and data analysis.
* **Reviews file**: file used in model that enable ranking by sentiment. 
* **Doc2Vec model** and **vector in a json file**: file used by  ```Doc2VecModel```.

If It's the first time all the needed file will be generated. However, this could take a long time.
Therefore, a pre-built version of every file is provided so, if everything downloaded correctly, it should be instant. 

**Please note that an error related to the searcher object may occur. In that case try to build again index running:** 
```
python main.py [-B | -S | -AS | -D2V] --build-index
```

## Project Structure

* ***assets***: directory containing images for graphic interface. 
* ***dataset***: the dataset. 
* ***doc2vec***: this package contains the implementation of ```Doc2VecModel```
* ***evaluation***: this package contains functions and queries for *benchmarks.ipynb*.
* ***gui***: this package contains the GUI code. 
* ***indexdir***: directory containing the index. 
* ***sentiment***: this package contains the implementation of ```AdvancedSentimentWeightingModel``` and ```SentimentWeightingModel```
* ***benchmarks.ipynb***: notebook to run benchmarks
* ***controller\.py***: file serves as the central hub for interacting with and orchestrating the functionalities of various other files within a software project. 
* ***index\.py***: this file builds setup the *schema* and then build the *index* which is stored in the *indexdir* directory. 
* ***main\.py***: run the program. 
* ***model\.py***: carry out the actual search function after having appropriately selected the model.
* ***config\.py***: stores configuration settings and parameters for the search-engine. 




