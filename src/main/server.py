import os

import time
import xmltodict
from flask import Flask, request, send_from_directory

from jsonInDB import *
from run import wechat

app = Flask(__name__)

root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..')
print root_dir


class User(dict):
  def __init__(self, id=None, data=None):
    super(User, self).__init__()
    if id:
      self.update(wechat.get_user_info(id))
    elif data:
      self.update(data)
      self['_id'] = str(self['_id'])

    else:
      raise ValueError("not value to initiate user")

  def get_id(self):
    return self['openid']

  def get_nickname(self):
    return self['nickname']


class WechatData(object):
  def __init__(self, raw_data):
    self._data = xmltodict.parse(raw_data)

  def __str__(self):
    return str(self._data)

  def get_event(self):
    try:
      return self._data['xml']['Event']
    except KeyError:
      return None

  def get_msg_type(self):
    try:
      return self._data['xml']['MsgType']
    except KeyError:
      return None

  def is_subscribe_event(self):
    return self.get_event() == 'subscribe' and self.get_msg_type() == 'event'

  def is_text_msg(self):
    return self.get_msg_type() == 'text'

  def get_from_user_name(self):
    try:
      return self._data['xml']['FromUserName']
    except KeyError:
      return None

  def get_content(self):
    try:
      return self._data['xml']['Content']
    except KeyError:
      return None


class UserManager(object):
  def __init__(self):
    # Map from user id to User
    self._all_users = {}

  def has_user(self, user_id):
    return user_id in self._all_users

  def add_user(self, user_id):
    if not self.has_user(user_id):
      self._all_users[user_id] = User(user_id)

  def process_new_user(self, user_id):
    if user_id not in self._all_users:
      self._all_users[user_id] = User(id=user_id)
      return self._all_users[user_id]

  def process_existing_user(self, user):
    self._all_users[user.get_id()] = user

  def get_user(self, user_id):
    return self._all_users.get(user_id)


class Reservation(object):
  def __init__(self, user_id, time_to_reserve, num_guest):
    self.reserver = user_manager.get_user(user_id)
    self.checkin_time = time_to_reserve
    self.num_guest = num_guest
    self.timestamp = time.time()
    self.id = "{}_{}_{}".format(user_id, num_guest, self.timestamp)

    # self.id = hashlib.sha1("{}{}{}".format(user_id, time_to_reserve, num_guest)).hexdigest()


user_manager = UserManager()
queue = []


def add_to_reservation(user_id, num_guest):
  queue.append(Reservation(user_id, time.time(), num_guest))


@app.route("/")
def root():
  dir = os.path.join(root_dir, 'src/main/html')
  return send_from_directory(dir, 'index.html')


@app.route("/<path:path>")
def hello(path):
  dir = os.path.join(root_dir, 'src/main/html')
  return send_from_directory(dir, path)


@app.route("/verify", methods=['POST', 'GET'])
def verify():
  timestamp = request.args['timestamp']
  signature = request.args['signature']
  nonce = request.args['nonce']
  echostr = request.args.get('echostr')

  data = WechatData(request.data)

  if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
    user_id = data.get_from_user_name()
    user_manager.process_new_user(user_id)

    if data.is_text_msg():
      user = user_manager.get_user(user_id)
      # wechat.send_text_message(user.get_id(), "hello there, {}".format(user.get_nickname()))

      num_guest = None
      try:
        num_guest = int(data.get_content())
      except ValueError:
        pass

      if num_guest:
        add_to_reservation(user.get_id(), num_guest)

      print data.get_content()

    if echostr is not None:
      return echostr
    else:
      return ""
  else:
    return "fail"


@app.route('/api/reservations/', methods=['GET', 'POST'])
def reservations():
  if request.method == 'GET':
    print queue
    return json.dumps(queue, default=lambda obj: obj.__dict__)
  # elif request.method == 'POST':
  #   print request.data
  #   return "hello"



@app.route('/api/reservations/ops', methods=['POST'])
def reservation_ops():
  def delete(reservation_id, a_queue):
    for reservation in a_queue:
      if reservation.id == reservation_id:
        a_queue.remove(reservation)

  op_name_to_methods = {
    'delete': delete
  }
  method = op_name_to_methods[request.form['op']]
  method(request.form['id'], queue)

  return "hello"

@app.route('/message/', methods=['POST'])
def message():
  data = xmltodict.parse(request.data)
  print data.get('FromUserName')
  # return render_template('args_action.html', name=name, email=email)
  return "Hello"


if __name__ == "__main__":
  user_ids = ["odIgav434SsjB4x8ROU7BJWzI5IU", "odIgav6fGLauJA1ukAtV_lGWWCPY", "odIgavz5qd3QrLSHyK5nefTgyIH4"]
  for user_id in user_ids:
    user_data = db.user.find_one({'openid': user_id})
    if user_data is not None:
      user = User(data=user_data)
      user_manager.process_existing_user(user)
    else:
      user = user_manager.process_new_user(user_id)
      db.user.save(user)

    add_to_reservation(user_id, 2)

  app.run('0.0.0.0', 5000, debug=True)

  # app.run('0.0.0.0', 80)
