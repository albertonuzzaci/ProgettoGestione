import pandas as pd
import random, json
import os, glob
def floatConverter(var):
    try:
        return float(var)
    except ValueError:
        return None

def intConverter(var):
    try:
        return int(var)
    except ValueError:
        return None

def bathConverter(var):
    try:
        return var.split()[0]
    except AttributeError:
        return None

def retAmenities(var):
    try:
        return bytes(var[1:-1].replace("\"",""), 'utf-8').decode('unicode-escape').split(", ")
    except:
        return None
def retPrice(var):
    try:
        return float(var[1:])
    except:
        return None
if __name__ == "__main__":
    
    information = {
        "neighbourhood":{}
    }
    max = -1.0
    min = 999.0
    for i in os.listdir("./dataset/json/"):
        with open(f'./dataset/json/{i}', "r") as f:
            dati = json.load(f)
            if dati["price"] != None:
                if float(dati["price"]) >= max:
                    max = dati["price"]
                    if float(dati["price"]) == 999.0:
                        print(f"./dataset/json/{dati["id"]}.json")
                if float(dati["price"]) <= min:
                    min = dati["price"]
                    if float(dati["price"]) == 0:
                        print(f"./dataset/json/{dati["id"]}.json")
            if dati["neighbourhood_cleansed"] != None:
                information["neighbourhood"][dati["neighbourhood_cleansed"]] = information["neighbourhood"].get(dati["neighbourhood_cleansed"], 0) + 1
    
    with open(f'./dataset/information.json','w') as f:
        information["max"] = max
        information["min"] = min
        json.dump(information, f)
        

    '''
    
    counterLess5 = 0
    counterLess4 = 0
    counterLess3 = 0
    counterLess2 = 0
    for i in os.listdir("./dataset/dataset_json"):
        with open(f'./dataset/dataset_json/{i}', "r") as f:
            dati = json.load(f)
        if dati["number_of_reviews_showed"] < 4:
            os.remove(f'./dataset/dataset_json/{i}')

            
    
    
    
    df = pd.read_csv("dataset/reviews.csv")
    for i, row in df.iterrows():
        try:
            
            with open(f'./dataset/dataset_json/{row["listing_id"]}.json', "r") as f:
                dati = json.load(f)
                if len(dati["reviews"]) < dati["number_of_reviews_showed"]:

                    dati["reviews"].append({
                    "date": row["date"],
                    "name": row["reviewer_name"],
                    "review": row["comments"]
                    })
                
            with open(f'./dataset/dataset_json/{row["listing_id"]}.json', "w") as f:
                json.dump(dati, f)
        except FileNotFoundError:
            print(row["listing_id"])
            
    
    for i, row in df.iterrows():
       
        entry = {
            "id": row["id"],
            "listing_url": row["listing_url"],
            "name": row["name"],
            "description": row["description"],
            "host_name": row["host_name"],
            "host_id": intConverter(row["host_id"]),
            "host_url": row["host_url"],
            "host_picture_url": row["host_picture_url"],
            "neighbourhood_cleansed": row["neighbourhood_cleansed"],
            "latitude": floatConverter(row["latitude"]),
            "longitude": floatConverter(row["longitude"]),
            "property_type": row["property_type"],
            "room_type": row["room_type"],
            "accommodates": row["accommodates"],
            "bathrooms": bathConverter(row["bathrooms_text"]),
            "bedrooms": intConverter(row["bedrooms"]),
            "beds": intConverter(row["beds"]),
            "amenities": retAmenities(row["amenities"]),
            "price": retPrice(row["price"]),
            "number_of_reviews": row["number_of_reviews"],
            "number_of_reviews_showed": random.randint(5, 15),
            "review_scores_rating": row["review_scores_rating"],
            "reviews": []
        }
            
                
        with open(f'./dataset/dataset_json/{entry["id"]}.json', "w") as outfile:
            json.dump(entry, outfile)
        '''
        
            
        
    
    