from threading import Thread

from polls.src.main.run import wechat


def async_send_message(open_id, text):
  t = Thread(target=send_message, args=(open_id, text))
  t.start()


def send_message(username, text):
  wechat.send_text_message(username, text)