from server import *
from jsonInDB import *
from bson.objectid import ObjectId
import pprint

client = MongoClient()
db = client.test

class testDAO:
  @staticmethod
  def insert_user(user_ids):
  #insert a record
      for user_id in user_ids:
        user_data = db.guest.find_one({'openid': user_id})
        if user_data is not None:
          user = User(data=user_data)
          user_manager.process_existing_user(user)
        else:
          user_manager.process_new_user(user_id)
          user = user_manager.get_user(user_id)
          result = db.guest.save(user);

  @staticmethod
  def insert_res(user_ids, num_guest):
      for user_id in user_ids:
        res = Reservation(user_id,time.time(),num_guest)
        res_infor = json.dumps(res,default=lambda obj:obj.__dict__)
        result = db.reservation.save(json.loads(res_infor));     
  @staticmethod
  def query_by_id(table, id):
      pprint.pprint(table.find_one({'_id': ObjectId(id)}));
      return table.find_one({'_id': ObjectId(id)})
  @staticmethod
  def query_by_user_id(table,id):
  # do a query based on id
      return table.find_one({'openid':id})
  @staticmethod    
  def delete_by_id(table,id):
      result = table.delete_many({'_id': ObjectId(id)})
  @staticmethod    
  def delete_all(table):
      result = table.delete_many({})
if __name__ == "__main__":
   t = testDAO()
 #  t.delete_all(db.user)
   users = ["odIgav434SsjB4x8ROU7BJWzI5IU", "odIgav6fGLauJA1ukAtV_lGWWCPY", "odIgavz5qd3QrLSHyK5nefTgyIH4"]
 #  t.insert_user(users)
 #  t.delete_all(db.reservation);
 #  t.insert_res(users,3)
   pprint.pprint(t.query_by_user_id(db.guest,'odIgavz5qd3QrLSHyK5nefTgyIH4'))
 #  pprint.pprint(t.query_by_id(db.guest,'56d3aed752e33074c4512b2e'))
#   cursor = db.guest.find()
#   for document in cursor:
#     pprint.pprint(document)
   


