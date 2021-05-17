# ADICIONAR FREQ ... [5,30,60,...]


# adicionar metodos para alterar os valores de cada daemon
# keys,campos, ... 
# 
# para aceder á db usar ... from api_daemon import db ou * 
# cada vez que se remove um daemon do backoffice se não tiver mais nenhum 
# remover dos daemons e da influx db?

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource,reqparse,abort
from sqlalchemy.dialects.postgresql import JSON
import json
import jwt
import datetime
from functools import wraps

# args format -> arg1,arg2,arg3|arg4|arg5 -> arg3 é um dict e obter os arg4 e arg5

def convert_args(args):
    pass
def read_args(args):
    pass


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATEBASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# __________________________ DB QUERYS _____________________________

# return basic url's
def get_basics():
    print('\n')
    print('\n')
    print('\n')
    print(Basic_url.query.all())
    print('\n')
    print('\n')
    print('\n')
    return Basic_url.query.all()
def check_basics_url(url):
    return Basic_url.query.filter(Basic_url.url == url).first()
def get_basic_status(val):
    return Key_url.query.filter_by(Basic_url.status==val)
def pause_basic(url):
    #Basic_url.update().where(Basic_url.url == url).values(status=False)
    Basic_url.query.filter(Basic_url.url == url).update({"status": False})
    db.session.commit()
def start_basic(url):
    Basic_url.query.filter(Basic_url.url == url).update({"status": True})
    db.session.commit()
# db_type -> url ou args ou val
def change_basic(url,db_type,val):
    print('\n')
    print('\n')
    print('\n')
    print(db_type)
    print('\n')
    print('\n')
    print('\n')
    
    Basic_url.query.filter(Basic_url.url == url).update({db_type: val})
    db.session.commit()
""" 
def change_basic_url(url,new_url):
    Basic_url.query.filter(Basic_url.url == url).update({"url": new_url})
    db.session.commit()
def change_basic_args(url,args):
    Basic_url.query.filter(Basic_url.url == url).update({"args": args})
    db.session.commit() 
"""
def remove_basic(url):
    Basic_url.query.filter(Basic_url.url == url).delete()
    db.session.commit()

   
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
# db_type -> url,args,key
def change_key(url,db_type,val):
    Key_url.query.filter(Key_url.url == url).update({db_type: val})
    db.session.commit()
""" 
def change_key_url(url,new_url):
    Key_url.query.filter(Key_url.url == url).update({"status": False})
    db.session.commit()
def change_key_args(url,args):
    Key_url.query.filter(Key_url.url == url).update({"status": False})
    db.session.commit()
def change_key_key(url,key):
    Key_url.query.filter(Key_url.url == url).update({"status": False})
    db.session.commit() 
"""
def remove_key(url):
    Key_url.query.filter(Key_url.url == url).delete()
    db.session.commit()

def get_tokens():
    return Token_url.query.all()
def check_tokens_url(url):
    return Token_url.query.filter(Token_url.url == url).first()
def get_token_status(val):
    return Key_url.query.filter_by(Token_url.status==val)
def pause_token(url):
    Token_url.query.filter(Token_url.url == url).update({"status": False})
def start_token(url):
    Token_url.query.filter(Token_url.url == url).update({"status": True})
def change_token(url,db_type,val):
    Key_url.query.filter(Token_url.url == url).update({db_type: val})
    db.session.commit()
""" 
def change_token_url(url,new_url):
    Key_url.query.filter(Key_url.url == url).update({"url": new_url})
    db.session.commit()
def change_token_args(url,args):
    Key_url.query.filter(Key_url.url == url).update({"args": args})
    db.session.commit()
def change_token_key(url,key):
    Key_url.query.filter(Key_url.url == url).update({"key": key})
    db.session.commit() 
def change_token_content(url,content_type):
    Key_url.query.filter(Key_url.url == url).update({"content": content_type})
    db.session.commit()
def change_token_auth(url,auth):
    Key_url.query.filter(Key_url.url == url).update({"author": auth})
    db.session.commit()
def change_token_secret(url,secret):
    Key_url.query.filter(Key_url.url == url).update({"secret": secret})
    db.session.commit() 
"""
def remove_token(url):
    Token_url.query.filter(Token_url.url == url).delete()
    db.session.commit()    
    
    
# ________________________ DB MODELS _______________________________
class Basic_url(db.Model):
    __tablename__ = 'Basic_url' 
    url = db.Column(db.String(500),primary_key=True,nullable=False,unique=True)
    args = db.Column(JSON,nullable=True)
    status = db.Column(db.Boolean(),nullable=False)
    def __repr__(self):
        return f"API(URL = {self.url}, args = {self.args}, status = {self.status})"
      
class Key_url(db.Model):
    __tablename__ = 'Key_url' 
    url = db.Column(db.String(500),primary_key=True,nullable=False,unique=True)
    args = db.Column(JSON,nullable=True)
    key = db.Column(db.String(300))
    status = db.Column(db.Boolean())
    def __repr__(self):
        return f"API(URL={self.url}, args={self.args}, status={self.status})"
    
class Token_url(db.Model):
    __tablename__ = 'Token_url' 
    url = db.Column(db.String(500),primary_key=True,nullable=False,unique=True)
    args = db.Column(JSON,nullable=True)
    key = db.Column(db.String(300))
    secret = db.Column(db.String(300))
    content_type = db.Column(db.String(50))
    auth_type = db.Column(db.String(50))
    status = db.Column(db.Boolean())
    def __repr__(self):
        return f"API(URL={self.url}, args={self.args}, status={self.status})"

db.create_all()
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
    if check_basics_url(request.args['url']):
        return "URL already exists",403
    
    aux = None
    if 'args' in request.args.keys():
        aux = request.args['args']
    
    basic_obj = Basic_url(url=request.args['url'],args=aux,status=True)
    db.session.add(basic_obj)
    db.session.commit()
    
    return "DAEMON RUNNING!",201

@app.route('/Daemon/Pause/Basic/<string:daemon_url>',methods=['GET'])
@token_required 
def api_pause_basic(daemon_url):
    if not check_basics_url(daemon_url):
        return "DAEMON URL NOT FOUND",403
    
    change_basic(daemon_url,"status",False)
    return "DAEMON PAUSED",201

@app.route('/Daemon/Start/Basic/<string:daemon_url>',methods=['GET'])
@token_required 
def api_start_basic(daemon_url):
    if not check_basics_url(daemon_url):
        return "DAEMON URL NOT FOUND",403
    
    change_basic(daemon_url,"status",True)
    return "DAEMON STARTED",201

@app.route('/Daemon/Print/Basic', methods=['GET'])
@token_required
def api_print_basics():
    get_basics()
    return "PRINTED",201

@app.route('/Daemon/Remove/Basic', methods=['GET'])
@token_required
def api_remove_basic():
    if not 'url' in request.args.keys():
        return 'Missing [url] Argument',400
    if not check_basics_url(request.args['url']):
        return 'DAEMON URL NOT FOUND',403
    
    remove_basic(request.args['url'])
    return 'REMOVED',201

@app.route('/Daemon/Change/Basic/<string:daemon_url>',methods=['GET'])
@token_required 
def api_change_basic(daemon_url):
    if not check_basics_url(daemon_url):
        return "DAEMON URL NOT FOUND",403
    for db_type in [val for val in request.args.keys() if val!='url']: 
        change_basic(daemon_url,db_type,request.args[db_type])
    return "DAEMON STARTED",201


# ____________________________ KEY __________________________________
@app.route('/Daemon/Add/Key', methods=['GET'])
@token_required
def api_add_daemon_key():
    if 'url' not in request.args.keys():
        return "Missing [url] Argument",400
    if check_keys_url(request.args['url']):
        return 'URL already exists',403
    if 'key' not in request.args.keys():
        return "Missing [key] Argument",400
    
    aux = None
    if 'args' in request.args.keys():
        aux = request.args['args']
    
    key_obj = Key_url(url=request.args['url'],args=aux,status=True)
    db.session.add(key_obj)
    db.session.commit()
    
    return "DAEMON RUNNING!",201

@app.route('/Daemon/Pause/Key/<string:daemon_url>',methods=['GET'])
@token_required 
def api_pause_key(daemon_url):
    if not check_keys_url(daemon_url):
        return "Missing [url] Argument",400
    
    change_key(daemon_url,"status",False)
    return "DAEMON PAUSED",201

@app.route('/Daemon/Start/Key/<string:daemon_url>',methods=['GET'])
@token_required 
def api_start_key(daemon_url):
    if not check_keys_url(daemon_url):
        return "DAEMON URL NOT FOUND",403
    
    change_key(daemon_url,"status",True)
    return "DAEMON STARTED",201

@app.route('/Daemon/Print/Key', methods=['GET'])
@token_required
def api_print_keys():
    get_keys()
    return "PRINTED",201

@app.route('/Daemon/Remove/Key', methods=['GET'])
@token_required
def api_remove_key():
    if not 'url' in request.args.keys():
        return 'Missing [url] Argument',400
    if not check_keys_url(request.args['url']):
        return 'DAEMON URL NOT FOUND',403
    
    remove_key(request.args['url'])
    return 'REMOVED',201

@app.route('/Daemon/Change/Key/<string:daemon_url>',methods=['GET'])
@token_required 
def api_change_key(daemon_url):
    if not 'url' in request.args.keys():
        return 'Missing [url] Argument',400
    if not check_keys_url(daemon_url):
        return "DAEMON URL NOT FOUND",403
    for db_type in [val for val in request.args.keys() if val!='url']: 
        change_key(daemon_url,db_type,request.args[db_type])
    return "DAEMON STARTED",201


# ______________________________Token __________________________________

@app.route('/Daemon/Add/Token', methods=['GET'])
@token_required
def api_add_daemon_Token():
    if 'url' not in request.args.keys():
        return "Missing [url] Argument",400
    if check_tokens_url(request.args['url']):
        return 'URL Already Exists',403
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
    
    token_obj = Token_url(url=request.args['url'],args=aux,status=True)
    db.session.add(token_obj)
    db.session.commit()
    
    return "DAEMON RUNNING!",201

@app.route('/Daemon/Pause/Token/<string:daemon_url>',methods=['GET'])
@token_required 
def api_pause_token(daemon_url):
    if not check_tokens_url(daemon_url):
        return "DAEMON URL NOT FOUND",403
    
    change_token(daemon_url,"status",False)
    return "DAEMON PAUSED",201

@app.route('/Daemon/Start/Token/<string:daemon_url>',methods=['GET'])
@token_required 
def api_start_token(daemon_url):
    if not check_tokens_url(daemon_url):
        return "DAEMON URL NOT FOUND",403
    
    change_token(daemon_url,"status",True)
    return "DAEMON STARTED",201

@app.route('/Daemon/Print/Token', methods=['GET'])
@token_required
def api_print_tokens():
    get_tokens()
    return "PRINTED",201

@app.route('/Daemon/Remove/Token', methods=['GET'])
@token_required
def api_remove_token():
    if not 'url' in request.args.tokens():
        return 'Missing [url] Argument',400
    if not check_tokens_url(request.args['url']):
        return 'DAEMON URL NOT FOUND',403
    
    remove_token(request.args['url'])
    return 'REMOVED',201

@app.route('/Daemon/Change/Token/<string:daemon_url>',methods=['GET'])
@token_required 
def api_change_token(daemon_url):
    if not 'url' in request.args.keys():
        return 'Missing [url]',400
    if not check_keys_url(daemon_url):
        return "DAEMON URL NOT FOUND",403
    for db_type in [val for val in request.args.keys() if val!='url']: 
        change_key(daemon_url,db_type,request.args[db_type])
    return "DAEMON STARTED",201


# SQL ABORTS


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