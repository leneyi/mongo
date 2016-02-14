from flask import Flask, render_template, request, url_for
import json
import xmltodict
from run import wechat

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


class WechatData:
  def __init__(self, raw_data):
    self._data = xmltodict.parse(raw_data)

  def __str__(self):
    return str(self._data)

  def getEvent(self):
    try:
      return self._data['xml']['Event']
    except KeyError:
      return None

  def getMsgType(self):
    try:
      return self._data['xml']['MsgType']
    except KeyError:
      return None

  def is_subscribe_event(self):
    return self.getEvent() == 'subscribe' and self.getMsgType() == 'event'

  def is_text_msg(self):
    return self.getMsgType() == 'text'

  def get_from_user_name(self):
    try:
      return self._data['xml']['FromUserName']
    except KeyError:
      return None


class UserManager:
  def __init__(self):
    # Map from user id to UserData
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


user_manager = UserManager()


@app.route("/")
def hello():
  return "Hello World!"


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
    user_manager.process_user(data.get_from_user_name())

    if data.is_text_msg():
      user = user_manager.get_user(data.get_from_user_name())
      wechat.send_text_message(user.get_id(), "hello there, {}".format(user.get_nickname()))

    if echostr is not None:
      return echostr
    else:
      return ""
  else:
    return "fail"


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
