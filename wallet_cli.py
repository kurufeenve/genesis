from transaction import *
from tx_validator import *
from pending_pool import *
from serializer import *
import sqlite3
import cmd
import requests
import json

class Wallet_cli(cmd.Cmd):

    doc_header = '''
**********

Pitcoin wallet command line interface.
available commands are:
    new - generate new private and public keys.
    import - imports a private key type WIF from a file.
    send - forms a transaction and sends it.
    broadcast - sends transactions to the server.
    exit - exits the command line imterface.

For detailed information use 'help <command>'.

**********'''

    # conn = sqlite3.connect('memorypool.db')
    # c = conn.cursor()
    # c.execute('''CREATE TABLE IF NOT EXISTS Unconfirmed_transactions (tx TEXT)''')
    pool = PendingPool()
    try:
        listConf = open('storage/server_config', 'r').read().split('\n')
        ip = listConf[0]
        port = listConf[1]
    except:
        print('ERROR reading server_config file')
    
    def do_new(self, command):
        'Generates new private and public keys and displays them.'
        wallet = Wallet()
        private_key = wallet.GenPrivKey()
        wif = codecs.decode(base58.b58encode_check(bytes.fromhex('80' + private_key)))
        publick_key = wallet.privateKeyToPublicKey(private_key)
        address = wallet.pubKeyToAddress(publick_key)
        fd = open('address', 'w')
        fd.write(address)
        fd.close()
        fd = open('privatekey', 'w')
        fd.write(wif)
        fd.close()
        print('private key: ', private_key)
        print('publick key: ', wallet.privateKeyToPublicKey(private_key))
        print('address was saved in file address')

    def do_import(self, command): #import privatekey
        'imports a private key type WIF from a file.'
        wallet = Wallet()
        l = command.split(', ')
        if len(l) != 1:
            print("*** invalid number of arguments")
            return
        try:
            fd = open(l[0], 'r')
            __data = fd.read().strip()
            __hex = codecs.decode(binascii.hexlify(base58.b58decode(__data)), 'ascii').upper()
            if __hex[:2] == '80':
                address = wallet.pubKeyToAddress(wallet.privateKeyToPublicKey(__hex[2:-8]))
                print(address)
                fd = open('./address', 'w')
                #print("address = ", address)
                fd.write(address)
            else:
                print('Wrong prefix')
        except:
            print('Something went wrong')

    def do_send(self, command): #send 1to4yvjbUSJvUYKJ6JertB7nUBJvJEQXG, 0001
        
        '''
        forms a transaction and sends it.
        ex.. send <% Recipient Address%>, <% Amount%>
        '''

        l = command.split(', ')
        if len(l) != 2:
            print("*** invalid number of arguments")
            return
        fds = open('address', 'r')
        sender = fds.read()
        fds.close()
        balance = self.check_balance(sender)
        balance = 1000 # for developing. del this!!!
        if int(l[1]) <= balance:
            tx = Transaction(sender, l[0], l[1])
            txHash = tx.txHashCalc()
            __fdpk = open('privatekey', 'r')
            __pk = codecs.decode(binascii.hexlify(base58.b58decode(__fdpk.read().strip())), 'ascii')[2:-8]
            __fdpk.close()
            tx.signature, tx.pubkey = Wallet.signMessage(Wallet, __pk, txHash)
            tx.signature = codecs.decode(binascii.hexlify(tx.signature))
            stx = Serializer.serialize(Serializer, tx)
            self.pool.addInPool(stx)
        else:
            print('insufficient funds', '\nbalance = ', balance, '\namount = ', l[1])
        
        # if self.pool.addInPool(stx):
        #     print(stx)
            # self.c.execute('''INSERT INTO Unconfirmed_transactions(tx) VALUES (?)''', (stx,))
            # self.conn.commit()
            # self.c.execute('''SELECT * FROM Unconfirmed_transactions''')
            # print('from DB = ', self.c.fetchone())
            # print('Hurray!')
        # else:
        #     print('transaction was not inserten into the DB')
        
    def do_broadcast(self, command):

        '''sends post requests to server with transactions'''

        for stx in self.pool.unconfirmedTx:
            jstx = json.dumps(stx)
            requests.post('http://' + self.ip + ':' + self.port + '/transaction/new', data=jstx)
        
        # for stx in self.pool.unconfirmedTx:   
        #     self.pool.unconfirmedTx.remove(stx)

    def do_check_balance(self, command):

        '''checks the balance of an address'''
        
        print(self.check_balance(command))


    def do_printPool(self, command):
        r = requests.get('http://' + self.ip + ':' + self.port + '/transaction/pendings')
        print(r.text)

    def do_exit(self, command):
        'exits the command line imterface.'
        return True

    def check_balance(self, address):
        balance = 0
        des = Deserializer()
        try:
            fd = open('storage/blockchain', 'r')
            blocks = json.loads(fd.read())
        except:
            print('no blockchain available')
        for block in blocks:
            stxs = block.get('transactions')
            for stx in stxs:
                tx = des.deserialize(stx)
                if tx.sender == address:
                    balance -= int(tx.amount)
                if tx.recipient == address:
                    balance += int(tx.amount)
        return balance

if __name__ == '__main__':
    cli = Wallet_cli()
    cli.cmdloop()

    #  send 1to4yvjbUSJvUYKJ6JertB7nUBJvJEQXG, 1
    #  check_balance 1to4yvjbUSJvUYKJ6JertB7nUBJvJEQXG