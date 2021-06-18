
from flask import Flask, request, jsonify, make_response,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource,reqparse,abort
from sqlalchemy.dialects.postgresql import JSON
import json
import jwt
import datetime
from functools import wraps
#import os
from config import *

#print(Config.SECRET_KEY)
#print(Config.SQLALCHEMY_DATABASE_URI)

app = Flask(__name__)
#print(os.environ.get('DATABASE_URL') or \
#        'sqlite:///' + os.path.join(basedir, 'app.db'))
#basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
#        'sqlite:///' + os.path.join(basedir, 'daemons_db.db')

app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = Config.SECRET_KEY

db = SQLAlchemy(app)
api = Api(app)
   
    
# ________________________ DB MODELS _______________________________
class Basic_url(db.Model):
    metric_id = db.Column(db.Integer(),primary_key=True)
    url = db.Column(db.String(500),nullable=False)
    args = db.Column(db.String(750),nullable=True)
    period = db.Column(db.Integer())
    status = db.Column(db.Boolean(),nullable=False,default=True)
    def __repr__(self):
        return f"API(ID={self.metric_id},URL = {self.url}, period={self.period}, status = {self.status}, args={self.args})"
      
class Key_url(db.Model):
    metric_id = db.Column(db.Integer(),primary_key=True)
    url = db.Column(db.String(500),nullable=False)
    args = db.Column(db.String(750),nullable=True)
    period = db.Column(db.Integer())
    key = db.Column(db.String(300))
    status = db.Column(db.Boolean(),nullable=False,default=True)
    def __repr__(self):
        return f"API(ID={self.metric_id},URL={self.url}, period={self.period},status={self.status}, args={self.args})"
    
class Http_url(db.Model):
    metric_id = db.Column(db.Integer(),primary_key=True)
    url = db.Column(db.String(500),nullable=False)
    args = db.Column(db.String(750),nullable=True)
    period = db.Column(db.Integer())
    key = db.Column(db.String(300))
    username = db.Column(db.String(300))
    status = db.Column(db.Boolean(),nullable=False,default=True)
    def __repr__(self):
        return f"API(ID={self.metric_id},URL={self.url}, period={self.period},status={self.status}, args={self.args})"  
    
class Token_url(db.Model):
    metric_id = db.Column(db.Integer(),primary_key=True)
    url = db.Column(db.String(500),nullable=False)
    token_url = db.Column(db.String(500),nullable=False)
    args = db.Column(db.String(750),nullable=True)
    period = db.Column(db.Integer())
    key = db.Column(db.String(300))
    secret = db.Column(db.String(300))
    content_type = db.Column(db.String(50))
    auth_type = db.Column(db.String(50))
    status = db.Column(db.Boolean(),nullable=False,default=True)
    def __repr__(self):
        return f"API(ID={self.metric_id},URL={self.url}, period={self.period}, status={self.status}, args={self.args})"

db.create_all()
#db.session.commit()

# __________________________ DB QUERYS _____________________________
class Query:
    # return basic url's
    def get_basic_args(val):
        return db.session.query(Basic_url.args,Basic_url.metric_id).filter(Basic_url.url==val,Basic_url.status==True).all()
    def get_basics():
        return Basic_url.query.all()
    def check_basics_id(val):
        return Basic_url.query.filter(Basic_url.metric_id == val).first()
    def get_basic_status(status):
        return Basic_url.query.filter_by(Basic_url.status==status)
    def pause_basic(val):
        Basic_url.query.filter(Basic_url.metric_id == val).update({"status": False})
        db.session.commit()
    def start_basic(val):
        Basic_url.query.filter(Basic_url.metric_id == val).update({"status": True})
        db.session.commit()
    def change_basic(val_id,db_type,val):
        Basic_url.query.filter(Basic_url.metric_id == val_id).update({db_type: val})
        db.session.commit()
    def remove_basic(val):
        Basic_url.query.filter(Basic_url.metric_id == val).delete()
        db.session.commit()
    def get_basic_period(freq):
        #return Basic_url.query.distinct(Basic_url.url).filter(Basic_url.status==True,Basic_url.period==freq).all()
        return db.session.query(Basic_url.url.distinct()).filter(Basic_url.status==True,Basic_url.period==freq).all()
    
    # return url's with keys
    def get_key_args(val):
        return db.session.query(Key_url.args,Key_url.metric_id).filter(Key_url.url==val,Key_url.status==True).all()
    def get_keys():
        return Key_url.query.all()
    def check_keys_id(val):
        return Key_url.query.filter(Key_url.metric_id == val).first()
    def get_key_status(status):
        return Key_url.query.filter_by(Key_url.status==status)
    def pause_key(val):
        Key_url.query.filter(Key_url.metric_id == val).update({"status": False})
        db.session.commit()
    def start_key(val):
        Key_url.query.filter(Key_url.metric_id == val).update({"status": False})
        db.session.commit()
    def change_key(val_id,db_type,val):
        Key_url.query.filter(Key_url.metric_id == val_id).update({db_type: val})
        db.session.commit()
    def remove_key(val):
        Key_url.query.filter(Key_url.metric_id == val).delete()
        db.session.commit()
    # só com status=True
    def get_key_period(freq):
        return Key_url.query.filter(Key_url.status==True,Key_url.period==freq).all()
    def get_key_period_distinct(freq):
        return db.session.query(Key_url.url.distinct(),Key_url.key).filter(Key_url.status==True,Key_url.period==freq).all()
    
    def get_http_args(val):
        return db.session.query(Http_url.args,Http_url.metric_id).filter(Http_url.url==val,Http_url.status==True).all()
    def get_https():
        return Http_url.query.all()
    def check_http_id(val):
        return Http_url.query.filter(Http_url.metric_id == val).first()
    def get_http_status(status):
        return Http_url.query.filter_by(Http_url.status==status)
    def pause_http(val):
        Http_url.query.filter(Http_url.metric_id == val).update({"status": False})
        db.session.commit()
    def start_http(val):
        Http_url.query.filter(Http_url.metric_id == val).update({"status": False})
        db.session.commit()
    def change_http(val_id,db_type,val):
        Http_url.query.filter(Http_url.metric_id == val).update({db_type: val})
        db.session.commit()
    def remove_http(val):
        Http_url.query.filter(Http_url.metric_id == val).delete()
        db.session.commit()
    # só com status=True
    def get_http_period(freq):
        return Http_url.query.filter(Http_url.status==True,Http_url.period==freq).all()
    def get_http_period_distinct(freq):
        return db.session.query(Http_url.url.distinct(),Http_url.username,Http_url.key).filter(Http_url.status==True,Http_url.period==freq).all()


    def get_token_args(val):
        return db.session.query(Token_url.args,Token_url.metric_id).filter(Token_url.url==val,Token_url.status==True).all()
    def get_tokens():
        return Token_url.query.all()
    def check_token_id(val):
        return Token_url.query.filter(Token_url.metric_id == val).first()
    def get_token_status(status):
        return Token_url.query.filter_by(Token_url.status==status)
    def pause_token(val):
        Token_url.query.filter(Token_url.metric_id == val).update({"status": False})
    def start_token(val):
        Token_url.query.filter(Token_url.metric_id == val).update({"status": True})
    def change_token(val_id,db_type,val):
        Token_url.query.filter(Token_url.metric_id ==val_id).update({db_type: val})
        db.session.commit()
    def remove_token(val):
        Token_url.query.filter(Token_url.metric_id == val).delete()
        db.session.commit()    
    def get_token_period_distinct(freq):
        return db.session.query(Token_url.url.distinct(),Token_url.token_url,Token_url.auth_type,Token_url.content_type,Token_url.secret,Token_url.key).filter(Token_url.status==True,Token_url.period==freq).all()
    def get_token_period(freq):
        return Token_url.query.filter(Token_url.status==True,Token_url.period==freq).all()


"""
print('\n')
print('\n')
print('basic period 5')
print(Query.get_basic_period(5))
print('basic args')
print(Query.get_basic_args("http://services.web.ua.pt/parques/parques"))
print('\n')
print('\n')
print('\n')
print('key period 5')
print(Query.get_key_period(5))
print('key args')
print(Query.get_key_args("http://services.web.ua.pt/parques/parques"))
print('\n')
print('\n')
print('\n')
print('http period 5')
print(Query.get_http_period(5))
print('http args')
print(Query.get_http_args("http://services.web.ua.pt/parques/parques"))
print('\n')
print('\n')
print('\n')
print('token_freq 5')
print(Query.get_token_period(5))
print('token_args')
print(Query.get_token_args('https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=1000&firstResult='))
print('\n')
print('\n')
"""
#   AUTHENTICATION KEY
#app.config['SECRET_KEY'] = 'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'
@app.route('/login', methods=['GET'])
def login():
    auth = request.authorization
    if auth and auth.password == app.secret_key:
        token = jwt.enconde({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    
    #return make_response('User NOT Authenticated', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return 'User NOT Authenticated',401
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['Authorization']
        if not token:
            return jsonify({'message': 'Token is missing'}),403
        if token != app.secret_key:
            return jsonify({'message': 'Token is invalid'}),403
        
        """
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid'}),403         
        """
        
        return f(*args, **kwargs)
    return decorated

daemons = {1:{"name":"recolha de kpis", "metric": '1 hora', "url":"www.current.pt"},2:{"name":"recolha de kpis", "metric": '1 hora', "url":"www.lol.pt"}}


# ____________________________ BASIC __________________________________
@app.route('/Daemon/Add/Basic', methods=['GET'])
@token_required
def api_add_daemon_Basic():
    if 'id' not in request.args.keys():
        return "Missing [id] Argument",400
    if 'url' not in request.args.keys():
        return "Missing [url] Argument",400
    if Query.check_basics_id(request.args['id']):
        return "ID already exists",403
    
    aux = None
    if 'args' in request.args.keys():
        aux = request.args['args']
    
    period = 5 if not 'period' in request.args else request.args['period']
    
    basic_obj = Basic_url(metric_id=request.args['id'],url=request.args['url'],args=aux,period=period,status=True)
    db.session.add(basic_obj)
    db.session.commit()
    
    return "DAEMON RUNNING!",201

@app.route('/Daemon/Pause/Basic',methods=['GET'])
@token_required 
def api_pause_basic():
    if not 'id' in request.args.keys():
        return 'Missing [id] Argument',400
    if not Query.check_basics_id(request.args['id']):
        return "DAEMON ID NOT FOUND",403
    
    Query.change_basic(request.args['id'],"status",False)
    return "DAEMON PAUSED",201

@app.route('/Daemon/Start/Basic',methods=['GET'])
@token_required 
def api_start_basic():
    if not 'id' in request.args.keys():
        return 'Missing [id] Argument',400
    if not Query.check_basics_id(request.args['id']):
        return "DAEMON ID NOT FOUND",403
    
    Query.change_basic(request.args['id'],"status",True)
    return "DAEMON STARTED",201

@app.route('/Daemon/Print/Basic', methods=['GET'])
@token_required
def api_print_basics():
    print(Query.get_basics())
    return "PRINTED",201

@app.route('/Daemon/Remove/Basic', methods=['GET'])
@token_required
def api_remove_basic():
    if not 'id' in request.args.keys():
        return 'Missing [id] Argument',400
    if not Query.check_basics_id(request.args['id']):        
        return 'DAEMON ID NOT FOUND',403
    
    Query.remove_basic(request.args['id'])
    return 'REMOVED',201

@app.route('/Daemon/Change/Basic',methods=['GET'])
@token_required 
def api_change_basic():
    if not 'id' in request.args.keys():
        return 'Missing [id] Argument',400
    if not Query.check_basics_id(request.args['id']):
        return "DAEMON ID NOT FOUND",403
    for db_type in [val for val in request.args.keys() if val!='id']: 
        Query.change_basic(request.args['id'],db_type,request.args[db_type])
    return "DAEMON STARTED",201

@app.route('/Daemon/Basic/Period/<int:period>',methods=['GET'])
@token_required 
def api_period_basic(period):
    print(Query.get_basic_period(period))
    return "PRINTED DAEMONS FREQ 5",201
    

# ____________________________ KEY __________________________________
@app.route('/Daemon/Add/Key', methods=['GET'])
@token_required
def api_add_daemon_key():
    if 'id' not in request.args.keys():
        return "Missing [id] Argument",400
    if Query.check_keys_id(request.args['id']):
        return 'ID already exists',403
    if 'url' not in request.args.keys():
        return "Missing [url] Argument",400
    if 'key' not in request.args.keys():
        return "Missing [key] Argument",400
    
    aux = None
    if 'args' in request.args.keys():
        aux = request.args['args']
    
    period = 5 if not 'period' in request.args else request.args['period']
    
    key_obj = Key_url(metric_id=int(request.args['id']),url=request.args['url'],args=aux,period=period,key=request.args['key'],status=True)
    db.session.add(key_obj)
    db.session.commit()
    
    return "DAEMON RUNNING!",201

@app.route('/Daemon/Pause/Key',methods=['GET'])
@token_required 
def api_pause_key():
    if not 'id' in request.args.keys():
        return 'Missing [id] Argument',400
    if not Query.check_keys_id(request.args['id']):
        return "Missing [id] Argument",403
    
    Query.change_key(request.args['id'],"status",False)
    return "DAEMON PAUSED",201

@app.route('/Daemon/Start/Key',methods=['GET'])
@token_required 
def api_start_key():
    if not 'id' in request.args.keys():
        return 'Missing [id] Argument',400
    if not Query.check_keys_id(request.args['id']):
        return "DAEMON id NOT FOUND",403
    
    Query.change_key(request.args['id'],"status",True)
    return "DAEMON STARTED",201

@app.route('/Daemon/Print/Key', methods=['GET'])
@token_required
def api_print_keys():
    Query.get_keys()
    return "PRINTED",201

@app.route('/Daemon/Remove/Key', methods=['GET'])
@token_required
def api_remove_key():
    if not 'id' in request.args.keys():
        return 'Missing [id] Argument',400
    if not Query.check_keys_id(request.args['id']):
        return 'DAEMON ID NOT FOUND',403
    
    Query.remove_key(request.args['id'])
    return 'REMOVED',201

@app.route('/Daemon/Change/Key',methods=['GET'])
@token_required 
def api_change_key():
    if not 'id' in request.args.keys():
        return 'Missing [id] Argument',400
    if not Query.check_keys_id(request.args['id']):
        return "DAEMON ID NOT FOUND",403
    for db_type in [val for val in request.args.keys() if val!='id']: 
        Query.change_key(request.args['id'],db_type,request.args[db_type])
    return "DAEMON STARTED",201

@app.route('/Daemon/Key/Period/<int:period>',methods=['GET'])
@token_required 
def api_period_key(period):
    print(Query.get_key_period(period))
    return "PRINTED DAEMONS FREQ 5",201


# ______________________________ HTTP __________________________________

@app.route('/Daemon/Add/Http', methods=['GET'])
@token_required
def api_add_daemon_http():
    if 'id' not in request.args.keys():
        return "Missing [id] Argument",400
    if 'url' not in request.args.keys():
        return "Missing [url] Argument",400
    if Query.check_http_id(request.args['id']):
        return 'DAEMON ID already exists',403
    if 'key' not in request.args.keys():
        return "Missing [key] Argument",400
    if 'username' not in request.args.keys(): 
        return 'Missing [username] Argument',400
    aux = None
    if 'args' in request.args.keys():
        aux = request.args['args']
    
    period = 5 if not 'period' in request.args else request.args['period']
    
    http_obj = Http_url(metric_id=request.args['id'],url=request.args['url'],args=aux,period=period,key=request.args['key'],username=request.args['username'],status=True)
    db.session.add(http_obj)
    db.session.commit()
    
    return "DAEMON RUNNING!",201

@app.route('/Daemon/Pause/Http',methods=['GET'])
@token_required 
def api_pause_http():
    if not 'id' in request.args.keys():
        return 'Missing [id] Argument',400
    if not Query.check_http_id(request.args['id']):
        return 'DAEMON ID already exists',403
    
    Query.change_http(request.args['id'],"status",False)
    return "DAEMON PAUSED",201

@app.route('/Daemon/Start/Http',methods=['GET'])
@token_required 
def api_start_http():
    if not 'id' in request.args.keys():
        return 'Missing [id] Argument',400
    if not Query.check_http_id(request.args['id']):
        return "DAEMON ID NOT FOUND",403
    
    Query.change_http(request.args['id'],"status",True)
    return "DAEMON STARTED",201

@app.route('/Daemon/Print/Http', methods=['GET'])
@token_required
def api_print_https():
    Query.get_https()
    return "PRINTED",201

@app.route('/Daemon/Remove/Http', methods=['GET'])
@token_required
def api_remove_http():
    if not 'id' in request.args.keys():
        return 'Missing [id] Argument',400
    if not Query.check_http_id(request.args['id']):
        return 'DAEMON ID NOT FOUND',403
    
    Query.remove_http(request.args['id'])
    return 'REMOVED',201

@app.route('/Daemon/Change/Http',methods=['GET'])
@token_required 
def api_change_http():
    if not 'id' in request.args.keys():
        return 'Missing [id] Argument',400
    if not Query.check_http_id(request.args['id']):
        return "DAEMON ID NOT FOUND",403
    for db_type in [val for val in request.args.keys() if val!='id']: 
        Query.change_http(request.args['id'],db_type,request.args[db_type])
    return "DAEMON STARTED",201

@app.route('/Daemon/Http/Period/<int:period>',methods=['GET'])
@token_required 
def api_period_http(period):
    print(Query.get_http_period(period))
    return "PRINTED DAEMONS FREQ 5",201



# ______________________________Token __________________________________

@app.route('/Daemon/Add/Token', methods=['GET'])
@token_required
def api_add_daemon_Token():
    if 'id' not in request.args.keys():
        return "Missing [id] Argument",400
    if 'url' not in request.args.keys():
        return "Missing [url] Argument",400
    if Query.check_token_id(request.args['id']):
        return 'ID Already Exists',403
    if 'token_url' not in request.args.keys():
        return "Missing [token_url] Argument",400
    if 'key' not in request.args.keys():
        return "Missing [key] Argument",400
    if 'secret' not in request.args.keys():
        return "Missing [secret] Argument",400
    if 'content_type' not in request.args.keys():
        return "Missing [content_type] Argument",400
    if 'auth_type' not in request.args.keys():
        return "Missing [auth_type] Argument",400
    
    aux = None
    if 'args' in request.args.keys():
        aux = request.args['args']
    
    period = 5 if not 'period' in request.args else request.args['period']
    
    token_obj = Token_url(metric_id=request.args['id'],url=request.args['url'],token_url=request.args['token_url'],args=aux,period=period,status=True,key=request.args['key'],secret=request.args['secret'],content_type=request.args['content_type'],auth_type=request.args['auth_type'])
    db.session.add(token_obj)
    db.session.commit()
    
    return "DAEMON RUNNING!",201

@app.route('/Daemon/Pause/Token',methods=['GET'])
@token_required 
def api_pause_token():
    if 'id' not in request.args.keys():
        return "Missing [id] Argument",400
    if not Query.check_token_id(request.args['id']):
        return "DAEMON ID NOT FOUND",403
    
    Query.change_token(request.args['id'],"status",False)
    return "DAEMON PAUSED",201

@app.route('/Daemon/Start/Token',methods=['GET'])
@token_required 
def api_start_token():
    if 'id' not in request.args.keys():
        return "Missing [id] Argument",400
    if not Query.check_token_id(request.args['id']):
        return "DAEMON ID NOT FOUND",403

    Query.change_token(request.args['id'],"status",True)
    return "DAEMON STARTED",201

@app.route('/Daemon/Print/Token', methods=['GET'])
@token_required
def api_print_tokens():
    print(Query.get_tokens())
    return "PRINTED",201

@app.route('/Daemon/Remove/Token', methods=['GET'])
@token_required
def api_remove_token():
    if not 'id' in request.args.keys():
        return 'Missing [id] Argument',400
    if not Query.check_token_id(request.args['id']):
        return 'DAEMON ID NOT FOUND',403
    
    Query.remove_token(request.args['id'])
    return 'REMOVED',201

@app.route('/Daemon/Change/Token',methods=['GET'])
@token_required 
def api_change_token():
    if 'id' not in request.args.keys():
        return "Missing [id] Argument",400
    if not Query.check_token_id(request.args['id']):
        return "DAEMON id NOT FOUND",403

    for db_type in [val for val in request.args.keys() if val!='id']: 
        Query.change_token(request.args['id'],db_type,request.args[db_type])
    return "DAEMON STARTED",201

@app.route('/Daemon/Token/Period/<int:period>',methods=['GET'])
@token_required 
def api_period_token(period):
    print(Query.get_token_period(period))
    return "PRINTED DAEMONS FREQ 5",201

@app.route('/',methods=['GET'])
def home():
	return 'DAEMON_API'

if __name__ == "__main__":
    app.run(debug=False)
