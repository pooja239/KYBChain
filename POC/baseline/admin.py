from web3 import Web3
from web3.logs import STRICT, IGNORE, DISCARD, WARN

ENCODING = 'utf-8'
 
class admin:
    
    def __init__(self, _privateKey, _address, _userName, _registerAddress, _registerABI, _URL):
        
        self.profile = {}
        self.profile['private_key'] = _privateKey
        self.profile['address'] = _address
        self.profile['userName'] = _userName
        self.URL = _URL

        _web3M = Web3(Web3.HTTPProvider(self.URL))
        _RegisterSc = _web3M.eth.contract(address=_registerAddress, abi=_registerABI)
        self.contracts = {}
        self.contracts['marketplace'] = {'Address': _registerAddress, 'ABI': _registerABI, 'web3': _web3M, 'contract': _RegisterSc}
