from server import *
from jsonInDB import *
from bson.objectid import ObjectId
import pprint


def query_by_id(table, id):
  return table.find_one({'_id': ObjectId(id)})


def query_by_user_id(table, user_id):
  return table.find_one({'openid': user_id})


# user = User("odIgavz5qd3QrLSHyK5nefTgyIH4")
# a = Reservation(user,2,3)
users = ["odIgav434SsjB4x8ROU7BJWzI5IU", "odIgav6fGLauJA1ukAtV_lGWWCPY", "odIgavz5qd3QrLSHyK5nefTgyIH4"]

# print db.user.find_one({'openid': "odIgav434SsjB4x8ROU7BJWzI5IU"})
  # print user

for user_id in user_ids:
  user_data = db.user.find_one({'openid': user_id})
  if user_data is not None:
    user = User(data=user_data)
    user_manager.process_existing_user(user)
  else:
    user_manager.process_new_user(user_id)
    user = user_manager.get_user(user_id)
    db.user.save(user)


pprint.pprint(user_manager._all_users)
