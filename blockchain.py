
import hashlib, json, datetime, random, requests

from ipfs import IPFS

class Blockchain:

    chain = []
    data = []
    nodes = set()
    coordinator = False

    @staticmethod
    def initialize():
        with open('nodes.json') as file:
            Blockchain.nodes = json.load(file)
        if len(Blockchain.chain)==0:
            #genesis_block
            Blockchain.chain.append({
                'hexdigest':'0000051e80d31fe9109e04ca2074878de248338b670916fc402e0c4e378b5f00',
                'IpfsHash':'QmUWfZSo9YWNqHx5GYrGXpGJZBok5KDB7Q4JVgkub5JHQH'
            })

    @staticmethod
    def create_txn(txn_data):
        IpfsHash = IPFS.addJson(txn_data).json()['IpfsHash']
        Blockchain.add_data(IpfsHash)
        Blockchain.broadcast_txn(IpfsHash)
        return IpfsHash

    @staticmethod
    def create_block(nonce=0, previous_hash = '0000', data = []):
        while True:
            block = {
                'index' : len(Blockchain.chain)+1,
                'timestamp' : datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S'),
                'nonce' : nonce,
                'previous_hash' : previous_hash,
                'data' : data
            }
            hexdigest = Blockchain.hash_block(block)
            if str(hexdigest)[:4] == '0000':
                break
            else :
                nonce+=1

        IpfsHash = IPFS.addJson(block).json()['IpfsHash']
        Blockchain.add_block({'hexdigest':hexdigest,'IpfsHash':IpfsHash})
        Blockchain.broadcast_block(hexdigest, IpfsHash)
        return {'hexdigest':hexdigest,'IpfsHash':IpfsHash}

    @staticmethod
    def add_data(IpfsHash):
        Blockchain.data.append(IpfsHash)
        if len(Blockchain.data) >= 10:
            Blockchain.coordinator_function()

    @staticmethod
    def add_block(block):
        Blockchain.chain.append(block)
        ipfsBlock = IPFS.getJson(block['IpfsHash']).json()
        data = ipfsBlock['data']
        for txn in data:
            Blockchain.data.remove(txn)

    @staticmethod
    def hash_block(block):
        block = json.dumps(block, separators=(',',':')).encode()
        return hashlib.sha256(block).hexdigest()

    @staticmethod
    def get_by_hash(IpfsHash):
        response = IPFS.getJson(IpfsHash)
        return response

    @staticmethod
    def is_chain_valid():
        prev_hash = '0000'
        for block in Blockchain.chain:
            blockdata = IPFS.getJson(block['IpfsHash'])
            blockdata = json.loads(blockdata)
            if str(Blockchain.hash_block(blockdata))[:4] != '0000' or blockdata['previous_hash'] != prev_hash:
                return False
            prev_hash = Blockchain.hash_block(block)
        return True

    #decentralization
    """ 
    @staticmethod
    def add_node(address):
        parsed_url = urlparse(address)
        Blockchain.nodes.add(parsed_url.netloc)
    """

    @staticmethod
    def broadcast_txn(IpfsHash):
        for node in Blockchain.nodes:
            requests.get(f"http://{node}/api/post_txn/{IpfsHash}/")

    @staticmethod
    def broadcast_block(hexdigest, IpfsHash):
        for node in Blockchain.nodes:
            requests.get(f"http://{node}/api/post_block/{hexdigest}/{IpfsHash}/")

    @staticmethod
    def coordinator_function():
        if Blockchain.coordinator is True:
            node = list(Blockchain.nodes)[1]
            requests.get(f"http://{node}/api/create_block")

    @staticmethod
    def synchronize():
        longest_chain = None
        max_length = len(Blockchain.chain)
        for node in Blockchain.nodes:
            response = requests.get(f"http://{node}/api/get_chain")
            if response.ok:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and Blockchain.is_chain_valid():
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            Blockchain.chain = longest_chain
            return True

