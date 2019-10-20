from block import *
from transaction import *
from serializer import Serializer
import requests
import time
import sqlite3
import json

class Blockchain():

    '''One ring to rule them all,
one ring to find them,
One ring to bring them all
and in the darkness bind them.'''

    # conn = sqlite3.connect('blockchain.db')
    # c = conn.cursor()
    # c.execute('''CREATE TABLE IF NOT EXISTS Blockchain (block BLOB)''')
    complexity = 2
    nonce = 0
    try:
        listConf = open('storage/server_config', 'r').read().split('\n')
        ip = listConf[0]
        port = listConf[1]
    except:
        print('ERROR reading server_config file')

    def mine(self, block):

        block.nonce = self.nonce
        block.blockHashCalc(0)
        while block.blockhash[:self.complexity] != '0' * self.complexity:
            block.nonce += 1
            block.blockHashCalc(0)
        return block

    def resolve_conflicts(self, chain):

        # try:
        new_chain = []
        height = 0
        fd = open('storage/blockchain', 'r', encoding='utf-8')
        try:
            my_chain = json.loads(fd.read())
            my_height = len(my_chain)
        except:
            my_height = 0
            if self.is_valid_chain(chain) and len(chain) > my_height:
                for elem in chain[height:]:
                    new_chain.append(elem.__dict__)
                Json = json.dumps(new_chain)
                fd = open('storage/blockchain', 'w')
                fd.write(Json)
                fd.close()
                print('your chain was replaced by longer chain')
            else:
                print('good try')
            return
        fd.close()
        print('height before while = ', height, "\nmy_chain[height].get('blockhash') = ", my_chain[height].get('blockhash'), '\nchain[height].blockhash = ', chain[height].blockhash)
        for elem in chain:
            print('height = ', height, '\tmy_height = ', my_height)
            if height < my_height and my_chain[height].get('blockhash') == elem.blockhash:
                new_chain.append(my_chain[height])
                height = height + 1
                print('height but here = ', height)
            else:
                break
        if (height == 0):
            height = my_height
        print('height here = ', height)
        if self.is_valid_chain(chain) and len(chain) > my_height:
            for elem in chain[height:]:
                new_chain.append(elem.__dict__)
            Json = json.dumps(new_chain)
            fd = open('storage/blockchain', 'w')
            fd.write(Json)
            fd.close()
            print('your chain was replaced by longer chain')
        else:
            print('good try')
        print(len(my_chain), '\nheight = ', height)
        uchain = my_chain[height:my_height]
        # print('uchain = ', uchain)
        for block in uchain:
            stxs = block.get('transactions')
            for stx in stxs:
                print(stx)
                jstx = json.dumps(stx)
                print(jstx)
                requests.post('http://' + self.ip + ':' + self.port + '/transaction/new', data=jstx)
        # except:
        #     print('something went wrong')
    
    def is_valid_chain(self, blocks):

        for height, block in enumerate(blocks):
            blckhsh, rt = block.blockhash, block.block_root
            if (height == 0):
                block.blockHashCalc(1)
            else:
                block.blockHashCalc(0)
            if height > 0:
                if block.previous_hash != blocks[height - 1].blockhash:
                    print('block hash error around ', height - 1, ' and ', height, 'blocks')
                    return False
            if not self.check_hash(blckhsh):
                return False
            if block.blockhash != blckhsh or block.block_root != rt:
                return False
        return True

    def add_node(self, node):

        fd = open('storage/nodes', 'a')
        fd.write(node + '\n')
        # print("""add a new node to the list of nodes, accepts an URL without scheme
# like ‘192.168.0.2:5000'""")

    def genesis_block(self):

        __mk = open('minerWIF', 'r')
        __mpk = codecs.decode(binascii.hexlify(base58.b58decode(__mk.read())))[2:-8]
        wallet = Wallet()
        minerAddress = wallet.pubKeyToAddress(wallet.privateKeyToPublicKey(__mpk))
        stxs = []
        tx = Transaction('00000000000000000000000000000000', minerAddress, '0050')
        txHash = tx.txHashCalc()
        tx.signature, tx.pubkey = Wallet.signMessage(Wallet, __mpk, txHash)
        tx.signature = codecs.decode(binascii.hexlify(tx.signature))
        stxs.append(Serializer.serialize(Serializer, tx))
        genesis = Block(int(time.time()), '00000000000000000000000000000000', stxs)
        genesis.blockHashCalc(1)
        while genesis.blockhash[:self.complexity] != '0' * self.complexity:
            genesis.nonce += 1
            genesis.blockHashCalc(1)
        return genesis.__dict__

    # def submit_tx(self):

    #     print('''web api route for receiving transaction and push it to pending pool. The route is /transaction/new''')
    #     !!!!same in mining!!!!

    def check_hash(self, blockhash):

        zeros = 0
        for elem in blockhash:
            if elem != '0':
                break
            if elem == '0':
                zeros += 1
        if zeros == self.complexity:
            return True
        else:
            return False

if __name__ == '__main__':
    B = Blockchain()
    # B.genesis_block()
    # B.add_node('192.168.0.2:5000')
    # B.add_node('192.168.0.3:5000')
    # B.add_node('192.168.0.4:5000')
    B.resolve_conflicts(5)
