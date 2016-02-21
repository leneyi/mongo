from server import *
# user = User("odIgavz5qd3QrLSHyK5nefTgyIH4")
# a = Reservation(user,2,3)

user_manager.process_user("odIgav434SsjB4x8ROU7BJWzI5IU")
# user_manager.process_user("odIgav6fGLauJA1ukAtV_lGWWCPY")
# user_manager.process_user("odIgavz5qd3QrLSHyK5nefTgyIH4")
user = user_manager.get_user("odIgav434SsjB4x8ROU7BJWzI5IU")
add_to_reservation("odIgav434SsjB4x8ROU7BJWzI5IU", 1)

# add_to_reservation("odIgav6fGLauJA1ukAtV_lGWWCPY", 2)
# add_to_reservation("odIgavz5qd3QrLSHyK5nefTgyIH4", 3)

print queue
# print json.dumps(queue)