from serializer import *
import sqlite3

class PendingPool():

    '''PendingPool class checks whether the transaction is valid
and stores it in program memory'''

    unconfirmedTx = [] #all instances will have same pool

    def addInPool(self, stx):
        print(stx)
        tx = Deserializer.deserialize(Deserializer, stx)
        txHash = tx.txHashCalc()
        # print('!!!!!!!!!!!!!!', Validator.signatureVal(Validator, txHash.encode('utf-8'), tx.pubkey, tx.signature))
        # print('!!!!!!!!!!!!!!', "\ntxHash.encode('utf-8') = ", txHash.encode('utf-8'), '\ntx.pubkey = ', tx.pubkey, '\ntx.signature = ', tx.signature, '\n!!!!!!!!!!!!!!!!!!!')
        if not Validator.signatureVal(Validator, txHash.encode('utf-8'), tx.pubkey, tx.signature):
            return False
        if not Validator.senderAddrVal(Validator, tx.pubkey, tx.sender):
            return False
        elif int(tx.amount) < 0:
            return False
        else:
            self.unconfirmedTx.append(stx)
            print('transaction was added to the mempool')
            return self.unconfirmedTx[-3:]
    
    def delFromPool(self, stx):
        try:
            self.unconfirmedTx.remove(stx)
            print('transaction was removed')
        except:
            print('ther is no such transaction in the mempool')
