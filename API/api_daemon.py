#   API usada para gerir os daemons apartir do backoffice
#   a informação dos deamons vai tar disponivél numa database (sql)
#   com a lista dos daemons por utilizador.
#   cada utilizador vai poder fazer diferentes operações 
#   com os seus daemons
#   podemos ter a api a gerar random keys e a enviar para a api do backoffice cada dia
#   para mudar a key

from flask import Flask, request, jsonify, make_response
from flask_restful import Api,Resource,reqparse,abort
import json
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
api = Api(app)


#   AUTHENTICATION TOKEN
app.config['SECRET_KEY'] = 'ads786zxc!SAD$sadz#xc'

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



# adicionar mensagens caso os args estejam mal etc ...



"""
    id -> static given by app or database ...
    name -> str
    description -> str
    metric -> str
    url -> str
"""
daemons = {1:{"name":"recolha de kpis", "metric": '1 hora', "url":"www.current.pt"},2:{"name":"recolha de kpis", "metric": '1 hora', "url":"www.lol.pt"}}

# daemon_put_args = reparse.RequestParser()
# daemon_put_args.add_argument("id",type=str,help="Error: send Daemon ID")
# daemon_put_args.add_argument("type",type=str,help="Error: send Daemon type")
# daemon_put_args.add_argument("metric",type=str,help="Error: send Daemon metric")


def abort_if_daemon_doesnt_exist(daemon_id):
    if daemon_id not in daemons:
        abort(404, message="daemon {} doesn't exist".format(daemon_id))
        
def abort_if_daemon_exist(daemon_id):
    if daemon_id in daemons:
        abort(404, message="daemon {} already exist's".format(daemon_id))

def abort_if_daemon_empty():
    if len(daemons)==0:
        abort(404, message="no daemon available")
"""
    def launch_process(self):
        pass

    def pause_process(self):
        pass

    def delete_process(self):
        pass

    def show_processes(self):
        pass 

    def show_activeProcesses(self):
        pass

    def show_pausedProcesses(self):
        pass
"""  
  
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
@app.route('/Daemon/Add', methods=['GET'])
@token_required
def api_add_daemon():
    pass

# pausar um daemon
@app.route('/Daemon/Pause/<int:daemon_id>', methods=['GET'])
@token_required
def api_pause_daemon():
    pass

@app.route('/Daemon/wut2', methods=['GET','POST'])
def api_all2():
    # if methods == "POST": ...
    
    return {},200
    
api.add_resource(Daemon_ID,"/Daemon/<int:daemon_id>")
#api.add_resource(Daemon_List,"/Daemon/Configure")
#api.add_resource(Daemon_Update,"/Daemon/update")

if __name__ == "__main__":
    app.run(debug=True)