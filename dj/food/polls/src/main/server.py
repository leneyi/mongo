import os

import time
import xmltodict

# from jsonInDB import *
from run import wechat

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



