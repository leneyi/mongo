# wechat_app
* Setup virtual environment for python
```
pip install virtualenv
virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
git clone https://github.com/wisechengyi/wechat_app.git
pip install -r wechat_app/requirements.txt
```

* Run the server
```
source venv/bin/activate
cd wechat_app/dj/food
./manage.py runserver
```
