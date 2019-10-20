from miner_cli import *
from wallet_cli import *

def premine():

        'creates 3 different addresses, sends 30 random transactions and mines 10 blocks'

        # miner key
        wallet = Wallet()
        private_key = wallet.GenPrivKey()
        wif = codecs.decode(base58.b58encode_check(bytes.fromhex('80' + private_key)))
        fd = open('minerWIF', 'w')
        fd.write(wif)
        fd.close()
        publick_key = wallet.privateKeyToPublicKey(private_key)
        address = wallet.pubKeyToAddress(publick_key)
        fd = open('minerAddress', 'w')
        fd.write(address)
        fd.close()
        
        # Alice
        private_key = wallet.GenPrivKey()
        wif = codecs.decode(base58.b58encode_check(bytes.fromhex('80' + private_key)))
        fd = open('AliceWIF', 'w')
        fd.write(wif)
        fd.close()
        publick_key = wallet.privateKeyToPublicKey(private_key)
        address = wallet.pubKeyToAddress(publick_key)
        fd = open('AliceAddress', 'w')
        fd.write(address)
        fd.close()

        # Bob
        private_key = wallet.GenPrivKey()
        wif = codecs.decode(base58.b58encode_check(bytes.fromhex('80' + private_key)))
        fd = open('BobWIF', 'w')
        fd.write(wif)
        fd.close()
        publick_key = wallet.privateKeyToPublicKey(private_key)
        address = wallet.pubKeyToAddress(publick_key)
        fd = open('BobAddress', 'w')
        fd.write(address)
        fd.close()

        # genesis block
        M_CLI = Miner_cli()
        M_CLI.genesis()

        # forming trnsactions
        W_CLI = Wallet_cli()
        sender = open('minerAddress', 'r').read()
        Alice = open('AliceAddress', 'r').read()
        Bob = open('BobAddress', 'r').read()
        i = 0
        while i < 30:
            if i % 2 == 0:
                balance = W_CLI.check_balance(sender)
                if 1 <= balance:
                    tx = Transaction(sender, Alice, '0001')
                    txHash = tx.txHashCalc()
                    __fdpk = open('minerWIF', 'r')
                    __pk = codecs.decode(binascii.hexlify(base58.b58decode(__fdpk.read().strip())), 'ascii')[2:-8]
                    __fdpk.close()
                    tx.signature, tx.pubkey = Wallet.signMessage(Wallet, __pk, txHash)
                    tx.signature = codecs.decode(binascii.hexlify(tx.signature))
                    stx = Serializer.serialize(Serializer, tx)
                    W_CLI.pool.addInPool(stx)
                else:
                    print('insufficient funds', '\nbalance = ', balance, '\namount = ', 1)
            else:
                if 1 <= balance:
                    tx = Transaction(sender, Bob, '0001')
                    txHash = tx.txHashCalc()
                    __fdpk = open('minerWIF', 'r')
                    __pk = codecs.decode(binascii.hexlify(base58.b58decode(__fdpk.read().strip())), 'ascii')[2:-8]
                    __fdpk.close()
                    tx.signature, tx.pubkey = Wallet.signMessage(Wallet, __pk, txHash)
                    tx.signature = codecs.decode(binascii.hexlify(tx.signature))
                    stx = Serializer.serialize(Serializer, tx)
                    W_CLI.pool.addInPool(stx)
                else:
                    print('insufficient funds', '\nbalance = ', balance, '\namount = ', 1)
            i = i + 1
        W_CLI.do_broadcast('broadcast')

        # mining blocks
        i = 0
        while i < 10:
            M_CLI.do_mine('mine')
            i = i + 1

if __name__ == '__main__':
    premine()