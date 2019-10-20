import hashlib

def merkle_root(transactions):
    root = []
    for txn in transactions:
        try:
            root.append(txn.encode())
        except:
            root.append(txn)
    l = len(root)
    if l > 1:
        if l % 2 != 0:
            root.append(root[-1])
            for elem in root:
                root[root.index(elem)] = hashlib.sha256(hashlib.sha256(elem).digest()).digest()
            root = [x+y for x,y in zip(root[0::2], root[1::2])]
            res = merkle_root(root)
        else:
            for elem in root:
                root[root.index(elem)] = hashlib.sha256(hashlib.sha256(elem).digest()).digest()
            root = [x+y for x,y in zip(root[0::2], root[1::2])]
            res = merkle_root(root)
    else:
        res = hashlib.sha256(hashlib.sha256(root[0]).digest()).hexdigest()
    return res

if __name__ == '__main__':
    res = merkle_root(['aa', 'bb', 'cc', 'dd', 'ee', 'nn', 'xx'])
    print(res)
