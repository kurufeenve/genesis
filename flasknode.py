from flask import Flask, request
from flask_restful import Resource, Api
from block import *
from wallet_cli import *
import json
import re

app = Flask(__name__)
api = Api(app)
pool = []
wcli = Wallet_cli()

try:
    listConf = open('storage/server_config', 'r').read().split('\n')
    ip = listConf[0]
    port = listConf[1]
except:
    print('ERROR reading server_config file')

class tx_new(Resource):
    
    def post(self):
        newtx = codecs.decode(request.data).strip('"')
        for tx in pool:
            if tx == newtx:
                return
        pool.append(newtx)
        return print("transaction was added to the server's pool")

class tx_mine(Resource):

    def get(self):
        
        reg = re.compile('\w+')
        if (len(pool) > 0):
            txs = pool[:3]
            print(pool[:3])
        else:
            return "NO transactions in the pool"
        try:
            fd = open('storage/nodes', 'r')
            nodes = fd.read()
            fd.close()
            nodelist = nodes.strip().split('\n')
            for node in nodelist:
                r = requests.get('http://' + node + '/transaction/pendings')
                node_pool = reg.findall(r.text)
                if Block.txValidator(Block, node_pool):
                    for dif_tx in set(node_pool).difference(pool):
                        pool.append(dif_tx)
        except:
            print("there are no nodes available. Are you sure you can trust anyone?")
        for elem in txs:
            pool.remove(elem)
        return txs
    
class pendings(Resource):
    
    def get(self):
        return pool

class del_pool(Resource):
    
    def get(self):
        pool.clear()
        return "pool was removed"

class chain(Resource):

    def get(self):
        try:
            return open('storage/blockchain', 'r').read()
        except:
            return "Error while reading. Check the file."

class chain_length(Resource):

    def get(self):

        try:
            fd = open('storage/blockchain', 'r')
            jchain = fd.read()
            fd.close()
            if not jchain:
                return 0
            chain = json.loads(jchain)
            chain_len = len(chain)
            return chain_len
        except:
            return "Error while reading. Check the file."

class block_last(Resource):

    def get(self):
        try:
            return json.dumps(json.loads(open('storage/blockchain', 'r').read())[-1])
        except:
            return "Error while reading. Check the file."

class get_pools(Resource):

    def get(self):

        reg = re.compile('\w+')
        try:
            fd = open('storage/nodes', 'r')
            nodes = fd.read()
            fd.close()
            nodelist = nodes.strip().split('\n')
            print(nodelist)
            for node in nodelist:
                r = requests.get('http://' + node + '/transaction/pendings')
                node_pool = reg.findall(r.text)
                print('node_pool = ', node_pool)
                if Block.txValidator(Block, node_pool):
                    for dif_tx in set(node_pool).difference(pool):
                        pool.append(dif_tx)
        except:
            print("there are no nodes available. Are you sure you can trust anyone?")

@app.route('/block')
def block():
    height = int(request.args.get('height'))
    try:
        return json.dumps(json.loads(open('storage/blockchain', 'r').read())[height])
    except:
        return "Error while reading. Check the file or parametr was not an integer in base10."

@app.route('/balance')
def balance():
    addr = request.args.get('addr')
    try:
        return str(wcli.check_balance(addr))
    except:
        return "Error. Something went wrong."


api.add_resource(tx_new, '/transaction/new')
api.add_resource(tx_mine, '/transaction/mine')
api.add_resource(pendings, '/transaction/pendings')
api.add_resource(get_pools, '/transaction/get_pools')
api.add_resource(del_pool, '/transaction/del')
api.add_resource(chain, '/chain')
api.add_resource(chain_length, '/chain/length')
api.add_resource(block_last, '/block/last')

if __name__ == '__main__':
    app.run(host=ip, port=port, debug=True)
