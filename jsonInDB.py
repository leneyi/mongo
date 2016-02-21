
#!/usr/bin/python
import json  
  
# dict to json  
d=dict(name="cui",age=20,score=88)  
print json.dumps(d)  
  
#list to json  
l=["cui",20,88]  
print json.dumps(l) 


#object to json  
class Guest(object):  

    def __init__(self, name, numberOfGuests, status):
        self.name = name
        self.numberOfGuests = numberOfGuests
        self.status = status
    
s = Guest('Bob', 10, "pending")
#lambda expression, argument:expression
gst =  json.dumps(s,default=lambda obj:obj.__dict__)
#print stu;



from pymongo import MongoClient 
 
client = MongoClient()
db = client.test
#insert into the collections
from datetime import datetime

# delete the collections
#result = db.guest.delete_many({})

#save document to collections
result = db.guest.save(json.loads(gst))

#result = db.guest.insert_one({"numberOfGuests": 20, "status": "pending", "name": "Bob"})

# search in the collections
cursor = db.guest.find()

# search with conditions in collections
#cursor = db.guest.find({"score":88})

for document in cursor:
    print(document)

