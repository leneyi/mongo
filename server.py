from flask import Flask, render_template, request, url_for
import json
import xmltodict
import run
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/verify", methods = ['POST', 'GET'])
def verify():
    #print request.args
    #return "verify"
    timestamp = request.args['timestamp']
    signature = request.args['signature']
    nonce = request.args['nonce']
    echostr = request.args.get('echostr')
    print request.method
    if run.wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        if echostr is not None:
	    return echostr
	elif request.method == 'POST':
	    msg = xmltodict.parse(request.data)
	    user_id = msg['xml']['FromUserName']
	    run.wechat.send_text_message(user_id, "hello there")
	    return ""
    else:
	return "fail"

@app.route('/message/', methods=['POST'])
def message():
    # name=request.args['yourname']
    # email=request.args['youremail']
    #print request.data
    print "data:", xmltodict.parse(request.data)
    # return render_template('args_action.html', name=name, email=email)
    return "Hello"

if __name__ == "__main__":
    app.run('0.0.0.0', 80, debug=True)


