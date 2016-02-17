# wechat_app
* Setup virtualvenv for python
```
pip install virtualenv
virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
```
* Run the server
```
git clone https://github.com/wisechengyi/wechat_app.git
cd wechat_app
pip install -r requirements.txt
$(which python) server.py (may need `sudo` depending on the server port
```
