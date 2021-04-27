#   API usada para gerir os daemons apartir do backoffice
#   a informação dos deamons vai tar disponivél numa database (sql)
#   com a lista dos daemons por utilizador.
#   cada utilizador vai poder fazer diferentes operações 
#   com os seus daemons
#

from flask import Flask, request
from flask_restful import Api,Resource,reqparse,abort
import json

app = Flask(__name__)
api = Api(app)


# adicionar mensagens caso os args estejam mal etc ...




"""
    id -> static given by app or database ...
    name -> str
    description -> str
    metric -> str
    url -> str
"""
daemons = {1:{"name":"recolha de kpis", "metric": '1 hora', "url":"www.current.pt"},3:{"name":"recolha de kpis", "metric": '1 hora', "url":"www.lol.pt"}}

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
    def get(self,daemon_id):
        abort_if_daemon_doesnt_exist(daemon_id)
        
        # pode dar um erro por ser um inteiro
        return json.dumps(daemons[daemon_id]),200 
    
    # apagar um daemon
    def delete(self):
        pass
"""    
class Daemon_Update(Resource):
    # alterar um url do daemon ou outro campo
    def get(self,daemon_id):
        abort_if_daemon_doesnt_exist(daemon_id)
        return json.dumps(daemons[daemon_id]),200
    
    # alterar o estado do daemon -> run/paused
    def patch(self,daemon_id):
        
        pass 
    
    def delete(self,daemon_id):
        pass    
"""
    

@app.route('/Daemon/list_all', methods=['GET'])
def api_all():
    return daemons,200


# alterar atributos do daemon
@app.route('/Daemon/update_url/<int:daemon_id>')
def api_update_url(daemon_id):
    abort_if_daemon_doesnt_exist(daemon_id)
    daemons[daemon_id]["url"] = request.args["url"]
    return daemons[daemon_id],200

@app.route('/Daemon/update_name/<int:daemon_id>')
def api_update_name(daemon_id):
    abort_if_daemon_doesnt_exist(daemon_id)
    daemons[daemon_id]["name"] = request.args["name"]
    return daemons[daemon_id],200

@app.route('/Daemon/update_description/<int:daemon_id>')
def api_update_description(daemon_id):
    abort_if_daemon_doesnt_exist(daemon_id)
    daemons[daemon_id]["description"] = request.args["description"]
    return daemons[daemon_id],200

@app.route('/Daemon/update_metric/<int:daemon_id>')
def api_update_metric(daemon_id):
    abort_if_daemon_doesnt_exist(daemon_id)
    daemons[daemon_id]["metric"] = request.args["metric"]
    return daemons[daemon_id],200


@app.route('/Daemon/wut2', methods=['GET','POST'])
def api_all2():
    # if methods == "POST": ...
    
    return {},200
    
api.add_resource(Daemon_ID,"/Daemon/<int:daemon_id>")
#api.add_resource(Daemon_List,"/Daemon/Configure")
#api.add_resource(Daemon_Update,"/Daemon/update")

if __name__ == "__main__":
    app.run(debug=True)