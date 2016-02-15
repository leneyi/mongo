from flask import Flask, render_template, request, url_for, send_from_directory
import json
import xmltodict
from run import wechat
import os, time

app = Flask(__name__)


class User:
  def __init__(self, id):
    self._id = id
    # print wechat.get_user_info(id)
    # self._user_info = json.load(wechat.get_user_info(id))
    self._user_info = wechat.get_user_info(id)
    # print self._user_info
    # print "type: {}".format(type(self._user_info))

  def get_id(self):
    return self._id

  def get_nickname(self):
    return self._user_info.get('nickname')

  def __repr__(self):
    return json.dumps(self, default=lambda o: o.__dict__)


class WechatData:
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

class UserManager:
  def __init__(self):
    # Map from user id to User
    self._all_users = {}

  def has_user(self, user_id):
    return user_id in self._all_users

  def add_user(self, user_id):
    if not self.has_user(user_id):
      self._all_users[user_id] = User(user_id)

  def process_user(self, user_id):
    if user_id not in self._all_users:
      self._all_users[user_id] = User(user_id)

  def get_user(self, user_id):
    return self._all_users.get(user_id)


class Reservation(dict):
  def __init__(self, user_id, time_to_reserve, num_guest):
    self['_reserver'] = user_id
    self['_checkin_time'] = time_to_reserve
    self['_num_guest'] = num_guest
    self['_timestamp'] = time.time()

user_manager = UserManager()

queue = []

def add_to_reservation(user_id, num_guest):
  queue.append(Reservation(user_id, time.time(), num_guest))

@app.route("/")
def root():
  return send_from_directory('html', 'index.html')


@app.route("/<path:path>")
def hello(path):
  return send_from_directory('html', path)


@app.route("/verify", methods=['POST', 'GET'])
def verify():
  timestamp = request.args['timestamp']
  signature = request.args['signature']
  nonce = request.args['nonce']
  echostr = request.args.get('echostr')

  data = WechatData(request.data)
  # print data


  # if data.is_subscribe_event():
  #   print "subscribe!"
  #   if data.get_from_user_name() is not None:
  #     all_users.add(User(data.get('FromUserName')))
  #     print all_users


  if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
    user_id = data.get_from_user_name()
    user_manager.process_user(user_id)

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

@app.route('/api/reservations/', methods=['GET'])
def reservations():
  print queue
  return json.dumps(queue)


@app.route('/message/', methods=['POST'])
def message():
  # name=request.args['yourname']
  # email=request.args['youremail']
  # print request.data
  data = xmltodict.parse(request.data)
  print data.get('FromUserName')
  # return render_template('args_action.html', name=name, email=email)
  return "Hello"


if __name__ == "__main__":
  app.run('0.0.0.0', 80, debug=True)
  # app.run('0.0.0.0', 80)
