import cmd
import requests
import json
from blockchain import *
import re

class Miner_cli(cmd.Cmd):

    doc_header = '''
**********

Pitcoin miner command line interface.
available commands are:
    mine - gathers transactions from the pool and forms a block.
    exit - exits the command line imterface.

For detailed information use 'help <command>'.

**********'''

    try:
        listConf = open('storage/server_config', 'r').read().split('\n')
        ip = listConf[0]
        port = listConf[1]
    except:
        print('ERROR reading server_config file')

    def do_mine(self, arg):

        'gathers transactions from the pool and forms a block.'

        blockchain = Blockchain()
        validator = Validator()
        blocks = list()
        reg = re.compile('\w+')
        try:
            fd = open('storage/blockchain', 'r', encoding='utf-8')
            blocks = json.loads(fd.read())
            fd.close()
        except:
            self.genesis()
            return

        try:
            fd = open('storage/blockchain', 'w')
            s = 'http://' + self.ip + ':' + self.port + '/transaction/mine'
            r = requests.get(s) #should check what server returns
            stxs = reg.findall(r.text)
            for stx in stxs:
                tx = Deserializer.deserialize(Deserializer, stx)
                txHash = tx.txHashCalc()
                if not validator.signatureVal(txHash.encode('utf-8'), tx.pubkey, tx.signature):
                    return False
            block = Block(int(time.time()), blocks[-1].get('blockhash'), stxs)
            block = blockchain.mine(block)
            blocks.append(block.__dict__)
            Json = json.dumps(blocks)
            fd.write(Json)
            fd.close()
           
        except:
            print('Something went wrong')

        

    def do_genesis(self, arg):

        'creates genesis block of the blockchain'

        self.genesis()

    def do_get_pools(self, arg):

        'scans other nodes for their pools'

        s = 'http://' + self.ip + ':' + self.port + '/transaction/get_pools'
        r = requests.get(s)
        print(r)

    def do_check_conflicts(self, arg):

        '''Checks all neibour nodes for chain length and compares with local chain.
Longest chain is validated and written to the local file if it is longer than local.'''

        self.check_confl()


    def genesis(self):

        blocks = list()
        blockchain = Blockchain()
        fd = open('storage/blockchain', 'w')
        block = blockchain.genesis_block()
        blocks.append(block)
        json.dump(blocks, fd)
        fd.close()

    def check_confl(self):
        
        BC = Blockchain()
        my_length = int(requests.get('http://' + self.ip + ':' + self.port + '/chain/length').text)
        print('my_length = ', my_length)
        # try:
        fd = open('storage/nodes', 'r')
        nodes = fd.read()
        fd.close()
        nodelist = nodes.strip().split('\n')
        for node in nodelist:
            big_length = my_length
            big_node = None
            length = int(requests.get('http://' + node + '/chain/length').text)
            print('node = ', node, '\nlength = ', length)
            if (length > my_length and length > big_length):
                big_node = node
                big_length = length
        print('big_node = ', big_node)
        if big_node:
            fd = open('buffer', 'w')
            jchain = str(requests.get('http://' + big_node + '/chain').text)
            fd.write(jchain)
            fd.close()
            chain = json.loads(json.loads(jchain))
            blocks = []
            for elem in chain:
                block = Block(elem.get('timestamp'), elem.get('previous_hash'), elem.get('transactions'))
                block.blockhash = elem.get('blockhash')
                block.block_root = elem.get('block_root')
                block.nonce = elem.get('nonce')
                blocks.append(block)
            BC.resolve_conflicts(blocks)
        else:
            print('Your chain is the longest, Master.')

        # except:
        #     print("there are no nodes available. Are you sure you can trust anyone?")

    def do_del_pool(self, arg):
        requests.get('http://' + self.ip + ':' + self.port + '/transaction/del')

    def do_exit(self, arg):

        'exits the command line imterface.'

        return True

if __name__ == '__main__':
    cli = Miner_cli()
    cli.cmdloop()
