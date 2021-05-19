# ADICIONAR FREQ ... [5,30,60,...]


# adicionar metodos para alterar os valores de cada daemon
# keys,campos, ... 
# 
# para aceder á db usar ... from api_daemon import db ou * 
# cada vez que se remove um daemon do backoffice se não tiver mais nenhum 
# remover dos daemons e da influx db?

from flask import Flask, request, jsonify, make_response,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource,reqparse,abort
from sqlalchemy.dialects.postgresql import JSON
import json
import jwt
import datetime
from functools import wraps
import os


app = Flask(__name__)
#print(os.environ.get('DATABASE_URL') or \
#        'sqlite:///' + os.path.join(basedir, 'app.db'))
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'daemons_db.db')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mnt/c/Users/alexg/OneDrive/Desktop/PEI/DAEMONS/Api/app.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\alexg\\Onedrive\\Desktop\\PEI\\DAEMONS\\Api\\daemon.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#C:\Users\alexg\OneDrive\Desktop\PEI\DAEMONS


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#db.init_app(app)
api = Api(app)
   
    
# ________________________ DB MODELS _______________________________
class Basic_url(db.Model):
    #__tablename__ = 'Basic_url' 
    url = db.Column(db.String(500),primary_key=True,nullable=False,unique=True)
    args = db.Column(db.String(750),nullable=True)
    period = db.Column(db.Integer())
    status = db.Column(db.Boolean(),nullable=False)
    def __repr__(self):
        return f"API(URL = {self.url}, period={self.period}, status = {self.status})"
      
class Key_url(db.Model):
    #__tablename__ = 'Key_url' 
    url = db.Column(db.String(500),primary_key=True,nullable=False,unique=True)
    args = db.Column(db.String(750),nullable=True)
    period = db.Column(db.Integer())
    key = db.Column(db.String(300))
    status = db.Column(db.Boolean())
    def __repr__(self):
        return f"API(URL={self.url}, period={self.period},status={self.status})"
    
class Http_url(db.Model):
    url = db.Column(db.String(500),primary_key=True,nullable=False,unique=True)
    args = db.Column(db.String(750),nullable=True)
    period = db.Column(db.Integer())
    key = db.Column(db.String(300))
    username = db.Column(db.String(300))
    status = db.Column(db.Boolean())
    def __repr__(self):
        return f"API(URL={self.url}, period={self.period},status={self.status})"  
    
class Token_url(db.Model):
    #__tablename__ = 'Token_url' 
    url = db.Column(db.String(500),primary_key=True,nullable=False,unique=True)
    token_url = db.Column(db.String(500),nullable=False)
    args = db.Column(db.String(750),nullable=True)
    period = db.Column(db.Integer())
    key = db.Column(db.String(300))
    secret = db.Column(db.String(300))
    content_type = db.Column(db.String(50))
    auth_type = db.Column(db.String(50))
    status = db.Column(db.Boolean())
    def __repr__(self):
        return f"API(URL={self.url}, period={self.period}, status={self.status})"

db.create_all()
#db.session.commit()

# __________________________ DB QUERYS _____________________________
class Query:
    # return basic url's
    def get_basics():
        return Basic_url.query.all()
    def check_basics_url(url):
        return Basic_url.query.filter(Basic_url.url == url).first()
    def get_basic_status(val):
        return Key_url.query.filter_by(Basic_url.status==val)
    def pause_basic(url):
        Basic_url.query.filter(Basic_url.url == url).update({"status": False})
        db.session.commit()
    def start_basic(url):
        Basic_url.query.filter(Basic_url.url == url).update({"status": True})
        db.session.commit()
    def change_basic(url,db_type,val):
        Basic_url.query.filter(Basic_url.url == url).update({db_type: val})
        db.session.commit()
    def remove_basic(url):
        Basic_url.query.filter(Basic_url.url == url).delete()
        db.session.commit()
    # só com status=True
    def get_basic_period(val=5):
        return Basic_url.query.filter(Basic_url.status==True,Basic_url.period==val).all()
    # ...
    
    
    # return url's with keys
    def get_keys():
        return Key_url.query.all()
    def check_keys_url(url):
        return Key_url.query.filter(Key_url.url == url).first()
    def get_key_status(val):
        return Key_url.query.filter_by(Key_url.status==val)
    def pause_key(url):
        Key_url.query.filter(Key_url.url == url).update({"status": False})
        db.session.commit()
    def start_key(url):
        Key_url.query.filter(Key_url.url == url).update({"status": False})
        db.session.commit()
    def change_key(url,db_type,val):
        Key_url.query.filter(Key_url.url == url).update({db_type: val})
        db.session.commit()
    def remove_key(url):
        Key_url.query.filter(Key_url.url == url).delete()
        db.session.commit()
    # só com status=True
    def get_key_period(val):
        return Key_url.query.filter(status=True,period=val).all()

    
    def get_http():
        return Http_url.query.all()
    def check_http_url(url):
        return Http_url.query.filter(Http_url.url == url).first()
    def get_http_status(val):
        return Http_url.query.filter_by(Http_url.status==val)
    def pause_http(url):
        Http_url.query.filter(Http_url.url == url).update({"status": False})
        db.session.commit()
    def start_http(url):
        Http_url.query.filter(Http_url.url == url).update({"status": False})
        db.session.commit()
    def change_http(url,db_type,val):
        Http_url.query.filter(Http_url.url == url).update({db_type: val})
        db.session.commit()
    def remove_http(url):
        Http_url.query.filter(Http_url.url == url).delete()
        db.session.commit()
    # só com status=True
    def get_http_period(val):
        return Http_url.query.filter(status=True,period=val).all()
    


    def get_tokens():
        return Token_url.query.all()
    def check_tokens_url(url):
        return Token_url.query.filter(Token_url.url == url).first()
    def get_token_status(val):
        return Token_url.query.filter_by(Token_url.status==val)
    def pause_token(url):
        Token_url.query.filter(Token_url.url == url).update({"status": False})
    def start_token(url):
        Token_url.query.filter(Token_url.url == url).update({"status": True})
    def change_token(url,db_type,val):
        Token_url.query.filter(Token_url.url == url).update({db_type: val})
        db.session.commit()
    def remove_token(url):
        Token_url.query.filter(Token_url.url == url).delete()
        db.session.commit()    
    # só com status=True
    def get_token_period(val):
        return Token_url.query.filter(Token_url.status==True,Token_url.period==val).all()
    # ...

#   AUTHENTICATION TOKEN
app.config['SECRET_KEY'] = 'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'
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

# daemon_put_args = reparse.RequestParser()
# daemon_put_args.add_argument("id",type=str,help="Error: send Daemon ID")
# daemon_put_args.add_argument("type",type=str,help="Error: send Daemon type")
# daemon_put_args.add_argument("metric",type=str,help="Error: send Daemon metric")

# ____________________________ BASIC __________________________________
@app.route('/Daemon/Add/Basic', methods=['GET'])
@token_required
def api_add_daemon_Basic():
    if 'url' not in request.args.keys():
        return "Missing [url] Argument",400
    if Query.check_basics_url(request.args['url']):
        return "URL already exists",403
    
    aux = None
    if 'args' in request.args.keys():
        aux = request.args['args']
    
    period = 5 if not 'period' in request.args else request.args['period']
    
    basic_obj = Basic_url(url=request.args['url'],args=aux,period=period,status=True)
    db.session.add(basic_obj)
    db.session.commit()
    
    return "DAEMON RUNNING!",201

@app.route('/Daemon/Pause/Basic/<string:daemon_url>',methods=['GET'])
@token_required 
def api_pause_basic(daemon_url):
    if not Query.check_basics_url(daemon_url):
        return "DAEMON URL NOT FOUND",403
    
    Query.change_basic(daemon_url,"status",False)
    return "DAEMON PAUSED",201

@app.route('/Daemon/Start/Basic/<string:daemon_url>',methods=['GET'])
@token_required 
def api_start_basic(daemon_url):
    if not Query.check_basics_url(daemon_url):
        return "DAEMON URL NOT FOUND",403
    
    Query.change_basic(daemon_url,"status",True)
    return "DAEMON STARTED",201

@app.route('/Daemon/Print/Basic', methods=['GET'])
@token_required
def api_print_basics():
    print(Query.get_basics())
    return "PRINTED",201

@app.route('/Daemon/Remove/Basic', methods=['GET'])
@token_required
def api_remove_basic():
    if not 'url' in request.args.keys():
        return 'Missing [url] Argument',400
    if not Query.check_basics_url(request.args['url']):
        return 'DAEMON URL NOT FOUND',403
    
    Query.remove_basic(request.args['url'])
    return 'REMOVED',201

@app.route('/Daemon/Change/Basic/<string:daemon_url>',methods=['GET'])
@token_required 
def api_change_basic(daemon_url):
    if not Query.check_basics_url(daemon_url):
        return "DAEMON URL NOT FOUND",403
    for db_type in [val for val in request.args.keys() if val!='url']: 
        Query.change_basic(daemon_url,db_type,request.args[db_type])
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
    if 'url' not in request.args.keys():
        return "Missing [url] Argument",400
    if Query.check_keys_url(request.args['url']):
        return 'URL already exists',403
    if 'key' not in request.args.keys():
        return "Missing [key] Argument",400
    
    aux = None
    if 'args' in request.args.keys():
        aux = request.args['args']
    
    period = 5 if not 'period' in request.args else request.args['period']
    
    key_obj = Key_url(url=request.args['url'],args=aux,period=period,key=request.args['key'],status=True)
    db.session.add(key_obj)
    db.session.commit()
    
    return "DAEMON RUNNING!",201

@app.route('/Daemon/Pause/Key/<string:daemon_url>',methods=['GET'])
@token_required 
def api_pause_key(daemon_url):
    if not Query.check_keys_url(daemon_url):
        return "Missing [url] Argument",400
    
    Query.change_key(daemon_url,"status",False)
    return "DAEMON PAUSED",201

@app.route('/Daemon/Start/Key/<string:daemon_url>',methods=['GET'])
@token_required 
def api_start_key(daemon_url):
    if not Query.check_keys_url(daemon_url):
        return "DAEMON URL NOT FOUND",403
    
    Query.change_key(daemon_url,"status",True)
    return "DAEMON STARTED",201

@app.route('/Daemon/Print/Key', methods=['GET'])
@token_required
def api_print_keys():
    Query.get_keys()
    return "PRINTED",201

@app.route('/Daemon/Remove/Key', methods=['GET'])
@token_required
def api_remove_key():
    if not 'url' in request.args.keys():
        return 'Missing [url] Argument',400
    if not Query.check_keys_url(request.args['url']):
        return 'DAEMON URL NOT FOUND',403
    
    Query.remove_key(request.args['url'])
    return 'REMOVED',201

@app.route('/Daemon/Change/Key/<string:daemon_url>',methods=['GET'])
@token_required 
def api_change_key(daemon_url):
    if not 'url' in request.args.keys():
        return 'Missing [url] Argument',400
    if not Query.check_keys_url(daemon_url):
        return "DAEMON URL NOT FOUND",403
    for db_type in [val for val in request.args.keys() if val!='url']: 
        Query.change_key(daemon_url,db_type,request.args[db_type])
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
    if 'url' not in request.args.keys():
        return "Missing [url] Argument",400
    if Query.check_keys_url(request.args['url']):
        return 'URL already exists',403
    if 'key' not in request.args.keys():
        return "Missing [key] Argument",400
    
    aux = None
    if 'args' in request.args.keys():
        aux = request.args['args']
    
    period = 5 if not 'period' in request.args else request.args['period']
    
    http_obj = Http_url(url=request.args['url'],args=aux,period=period,key=request.args['key'],status=True)
    db.session.add(http_obj)
    db.session.commit()
    
    return "DAEMON RUNNING!",201

@app.route('/Daemon/Pause/Http/<string:daemon_url>',methods=['GET'])
@token_required 
def api_pause_http(daemon_url):
    if not Query.check_keys_url(daemon_url):
        return "Missing [url] Argument",400
    
    Query.change_http(daemon_url,"status",False)
    return "DAEMON PAUSED",201

@app.route('/Daemon/Start/Http/<string:daemon_url>',methods=['GET'])
@token_required 
def api_start_http(daemon_url):
    if not Query.check_https_url(daemon_url):
        return "DAEMON URL NOT FOUND",403
    
    Query.change_http(daemon_url,"status",True)
    return "DAEMON STARTED",201

@app.route('/Daemon/Print/Http', methods=['GET'])
@token_required
def api_print_https():
    Query.get_https()
    return "PRINTED",201

@app.route('/Daemon/Remove/Http', methods=['GET'])
@token_required
def api_remove_http():
    if not 'url' in request.args.keys():
        return 'Missing [url] Argument',400
    if not Query.check_https_url(request.args['url']):
        return 'DAEMON URL NOT FOUND',403
    
    Query.remove_http(request.args['url'])
    return 'REMOVED',201

@app.route('/Daemon/Change/Http/<string:daemon_url>',methods=['GET'])
@token_required 
def api_change_http(daemon_url):
    if not 'url' in request.args.keys():
        return 'Missing [url] Argument',400
    if not Query.check_https_url(daemon_url):
        return "DAEMON URL NOT FOUND",403
    for db_type in [val for val in request.args.keys() if val!='url']: 
        Query.change_http(daemon_url,db_type,request.args[db_type])
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
    if 'url' not in request.args.keys():
        return "Missing [url] Argument",400
    if Query.check_tokens_url(request.args['url']):
        return 'URL Already Exists',403
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
    
    token_obj = Token_url(url=request.args['url'],token_url=request.args['token_url'],args=aux,period=period,status=True,key=request.args['key'],secret=request.args['secret'],content_type=request.args['content_type'],auth_type=request.args['auth_type'])
    db.session.add(token_obj)
    db.session.commit()
    
    return "DAEMON RUNNING!",201

@app.route('/Daemon/Pause/Token/<string:daemon_url>',methods=['GET'])
@token_required 
def api_pause_token(daemon_url):
    if not Query.check_tokens_url(daemon_url):
        return "DAEMON URL NOT FOUND",403
    
    Query.change_token(daemon_url,"status",False)
    return "DAEMON PAUSED",201

@app.route('/Daemon/Start/Token/<string:daemon_url>',methods=['GET'])
@token_required 
def api_start_token(daemon_url):
    if not Query.check_tokens_url(daemon_url):
        return "DAEMON URL NOT FOUND",403
    
    Query.change_token(daemon_url,"status",True)
    return "DAEMON STARTED",201

@app.route('/Daemon/Print/Token', methods=['GET'])
@token_required
def api_print_tokens():
    Query.get_tokens()
    return "PRINTED",201

@app.route('/Daemon/Remove/Token', methods=['GET'])
@token_required
def api_remove_token():
    if not 'url' in request.args.tokens():
        return 'Missing [url] Argument',400
    if not Query.check_tokens_url(request.args['url']):
        return 'DAEMON URL NOT FOUND',403
    
    Query.remove_token(request.args['url'])
    return 'REMOVED',201

@app.route('/Daemon/Change/Token/<string:daemon_url>',methods=['GET'])
@token_required 
def api_change_token(daemon_url):
    if not 'url' in request.args.tokens():
        return 'Missing [url]',400
    if not Query.check_tokens_url(daemon_url):
        return "DAEMON URL NOT FOUND",403
    for db_type in [val for val in request.args.keys() if val!='url']: 
        Query.change_token(daemon_url,db_type,request.args[db_type])
    return "DAEMON STARTED",201

@app.route('/Daemon/Token/Period/<int:period>',methods=['GET'])
@token_required 
def api_period_token(period):
    print(Query.get_token_period(period))
    return "PRINTED DAEMONS FREQ 5",201


# DAEMON ABORTS
def abort_if_daemon_doesnt_exist(daemon_id):
    if daemon_id not in daemons:
        abort(404, message="daemon {} doesn't exist".format(daemon_id))
        
def abort_if_daemon_exist(daemon_id):
    if daemon_id in daemons:
        abort(404, message="daemon {} already exist's".format(daemon_id))

def abort_if_daemon_empty():
    if len(daemons)==0:
        abort(404, message="no daemon available")

  
class Daemon_ID(Resource):
    
    # info do daemon(daemon_id)
    @token_required
    def get(self,daemon_id):
        abort_if_daemon_doesnt_exist(daemon_id)
        
        # pode dar um erro por ser um inteiro
        return json.dumps(daemons[daemon_id]),200 
    
    # apagar um daemon
    @token_required
    def delete(self,daemon_id):
        pass

# tirar o url da maneira sem key
@app.route('/Daemon/list_all', methods=['GET'])
@token_required
def api_all():
    return daemons,200


# alterar atributos do daemon
@app.route('/Daemon/update_url/<int:daemon_id>', methods=['GET'])
@token_required
def api_update_url(daemon_id):
    abort_if_daemon_doesnt_exist(daemon_id)
    daemons[daemon_id]["url"] = request.args["url"]
    return daemons[daemon_id],200

@app.route('/Daemon/update_name/<int:daemon_id>', methods=['GET'])
@token_required
def api_update_name(daemon_id):
    abort_if_daemon_doesnt_exist(daemon_id)
    daemons[daemon_id]["name"] = request.args["name"]
    return daemons[daemon_id],200

@app.route('/Daemon/update_description/<int:daemon_id>', methods=['GET'])
@token_required
def api_update_description(daemon_id):
    abort_if_daemon_doesnt_exist(daemon_id)
    daemons[daemon_id]["description"] = request.args["description"]
    return daemons[daemon_id],200

@app.route('/Daemon/update_metric/<int:daemon_id>', methods=['GET'])
@token_required
def api_update_metric(daemon_id):
    abort_if_daemon_doesnt_exist(daemon_id)
    daemons[daemon_id]["metric"] = request.args["metric"]
    return daemons[daemon_id],200

# adicionar um daemon
# testar dar launch ao daemon a partir desta função com os args -> url,key,args,request=1/0
# depois testar escrever no ficheiro com os args de cada daemon e ver se o daemon vai ler bem

    
    
api.add_resource(Daemon_ID,"/Daemon/<int:daemon_id>")
#api.add_resource(Daemon_List,"/Daemon/Configure")
#api.add_resource(Daemon_Update,"/Daemon/update")

if __name__ == "__main__":
    app.run(debug=True)