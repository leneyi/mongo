
from pymongo import MongoClient 

 
client = MongoClient()
db = client.test

from datetime import datetime
# insert into collections
result = db.restaurants.insert_one(
    {
        "address": {
            "street": "2 Avenue",
            "zipcode": "10075",
            "building": "1480",
            "coord": [-73.9557413, 40.7720266]
        },
        "borough": "Manhattan",
        "cuisine": "Italian",
        "grades": [
            {
                "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
                "grade": "A",
                "score": 11
            },
            {
                "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
                "grade": "B",
                "score": 17
            }
        ],
        "name": "Vella",
        "restaurant_id": "41704620"
    }
)

#print result.inserted_id

#update the content
result = db.restaurants.update_one(
    {"name": "Vella"},
    {
        "$set": {
            "cuisine": "American (New)"
        },
        "$currentDate": {"lastModified": True}
    }
)

print result.matched_count
#print db.collection_names()  
cursor = db.restaurants.find()
#cursor = db.restaurants.find({"borough": "Manhattan"})
#cursor = db.restaurants.find({"address.zipcode": "10075"})
for document in cursor:
    print(document)
#result = db.restaurants.delete_many({})
#print result.deleted_count
